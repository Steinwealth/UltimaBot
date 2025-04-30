import datetime

class TradeLogger:
    def __init__(self, db_session):
        self.db_session = db_session

    async def log_trade_open(self, trade_details, account_snapshot):
        """
        Logs trade entry into the database with capital allocation details.
        
        :param trade_details: Dict with trade info (trade_id, symbol, side, entry, etc.)
        :param account_snapshot: Dict with account capital details (buying_power, margin, etc.)
        """
        trade_record = {
            'trade_id': trade_details['trade_id'],
            'symbol': trade_details['symbol'],
            'side': trade_details['side'],
            'entry_price': trade_details['entry'],
            'take_profit': trade_details['take_profit'],
            'stop_loss': trade_details['stop_loss'],
            'confidence': trade_details['confidence'],
            'status': 'open',
            'timestamp_opened': datetime.datetime.utcnow(),
            # Capital Allocation Snapshot
            'account_balance': account_snapshot.get('balance'),
            'cash_available': account_snapshot.get('cash_available'),
            'buying_power': account_snapshot.get('buying_power'),
            'margin_balance': account_snapshot.get('margin_balance'),
            'margin_used': account_snapshot.get('margin_used'),
            'margin_enabled': account_snapshot.get('margin_enabled'),
            'margin_percent': account_snapshot.get('margin_percent')
        }
        await self.db_session.insert_trade(trade_record)

    async def log_trade_close(self, trade_details, exit_reason, close_price):
        """
        Logs trade exit into the database.
        
        :param trade_details: Dict with trade info (trade_id).
        :param exit_reason: String (e.g., 'take_profit', 'stop_loss', 'confidence_drop').
        :param close_price: Float, price at trade exit.
        """
        update_fields = {
            'status': 'closed',
            'exit_reason': exit_reason,
            'exit_price': close_price,
            'timestamp_closed': datetime.datetime.utcnow()
        }
        await self.db_session.update_trade(trade_details['trade_id'], update_fields)

    async def fetch_trade_history(self, symbol=None):
        """
        Retrieves trade history from the database.
        
        :param symbol: Optional string to filter by symbol.
        :return: List of trade records.
        """
        return await self.db_session.get_trade_history(symbol)
