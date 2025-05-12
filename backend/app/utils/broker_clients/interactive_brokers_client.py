from ib_insync import IB, util

class InteractiveBrokersClient:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1, test_mode=False):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False
        self.account_id = None
        self.test_mode = test_mode

    async def login(self):
        """
        Connect to IB TWS or IB Gateway.
        """
        if self.test_mode:
            self.connected = True
            return True

        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            self.connected = self.ib.isConnected()
            return self.connected
        except Exception as e:
            print(f"[InteractiveBrokersClient] Connection failed: {e}")
            self.connected = False
            return False

    async def is_logged_in(self):
        return self.connected

    async def get_account_info(self):
        """
        Fetch account balances from IB or return simulated data in test mode.
        """
        if self.test_mode:
            return {
                "account_id": "IB-654",
                "balance": 50000.00,
                "cash_available": 20000.00,
                "buying_power": 40000.00,
                "margin_balance": 10000.00,
                "margin_used": 3000.00,
                "margin_enabled": True,
                "margin_percent": 30.0
            }

        accounts = self.ib.managedAccounts()
        if not accounts:
            raise Exception("No IB accounts found.")

        self.account_id = accounts[0]
        account_summary = self.ib.accountSummary(account=self.account_id)

        balance = float(account_summary.loc['NetLiquidation']['value'])
        cash_available = float(account_summary.loc['AvailableFunds']['value'])
        buying_power = float(account_summary.loc['BuyingPower']['value'])
        margin_balance = float(account_summary.loc['EquityWithLoanValue']['value'])
        margin_used = balance - margin_balance
        margin_enabled = margin_balance > 0
        margin_percent = (margin_used / margin_balance) * 100 if margin_enabled else 0.0

        return {
            "account_id": self.account_id,
            "balance": balance,
            "cash_available": cash_available,
            "buying_power": buying_power,
            "margin_balance": margin_balance,
            "margin_used": margin_used,
            "margin_enabled": margin_enabled,
            "margin_percent": margin_percent
        }

    def disconnect(self):
        if self.ib.isConnected():
            self.ib.disconnect()
        self.connected = False
