# backend/engines/trade_tracking/trade_logger.py

import datetime

class TradeLogger:
    def __init__(self, db_session):
        self.db_session = db_session

    async def log_trade_open(self, trade_details, account_snapshot):
        """
        Logs trade entry into the database with capital allocation and metadata.
        """
        trade_record = {
            'trade_id': trade_details['trade_id'],
            'symbol': trade_details['symbol'],
            'side': trade_details['side'],
            'entry_price': trade_details['entry_price'],
            'take_profit': trade_details['take_profit'],
            'stop_loss': trade_details['stop_loss'],
            'confidence': trade_details['confidence'],
            'status': 'open',
            'timestamp_opened': datetime.datetime.utcnow(),
            'model_id': trade_details.get('model_id'),
            'strategy_id': trade_details.get('strategy_id'),
            'broker_id': trade_details.get('broker_id'),
            # Capital Allocation Snapshot
            'account_balance': account_snapshot.get('balance'),
            'cash_available': account_snapshot.get('cash_available'),
            'buying_power': account_snapshot.get('buying_power'),
            'margin_balance': account_snapshot.get('margin_balance'),
            'margin_used': account_snapshot.get('margin_used'),
            'margin_enabled': account_snapshot.get('margin_enabled'),
            'margin_percent': account_snapshot.get('margin_percent'),
            'allocation_amount': trade_details.get('size'),
        }
        await self.db_session.insert_trade(trade_record)

    async def log_trade_close(self, trade_details, exit_reason, close_price):
        """
        Logs trade exit into the database with performance metrics.
        """
        entry_price = trade_details.get('entry_price')
        size = trade_details.get('size', 1)

        if entry_price:
            gain_dollar = (close_price - entry_price) * size
            gain_pct = ((close_price - entry_price) / entry_price) * 100
        else:
            gain_dollar = None
            gain_pct = None

        update_fields = {
            'status': 'closed',
            'exit_reason': exit_reason,
            'exit_price': close_price,
            'timestamp_closed': datetime.datetime.utcnow(),
            'gain_dollar': round(gain_dollar, 2) if gain_dollar is not None else None,
            'gain_pct': round(gain_pct, 2) if gain_pct is not None else None,
        }
        await self.db_session.update_trade(trade_details['trade_id'], update_fields)

    async def fetch_trade_history(self, symbol=None):
        """
        Retrieves trade history from the database.
        """
        return await self.db_session.get_trade_history(symbol)
