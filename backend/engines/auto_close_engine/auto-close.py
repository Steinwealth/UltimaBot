 from datetime import datetime

class AutoCloseEngine:
    def __init__(self, broker_client, confidence_floor=0.93, confidence_drop_threshold=0.10, hero_mode_close_time=60, trail_to_moon_buffer=0.95, momentum_buffer=0.02):
        """
        :param broker_client: Broker client instance.
        :param confidence_floor: Absolute confidence floor (0.93).
        :param confidence_drop_threshold: Confidence drop % to trigger early closure.
        :param hero_mode_close_time: Time in minutes to auto-close profitable trades in Hero Mode.
        :param trail_to_moon_buffer: Buffer % of Forecast TP for activating Trail-to-Moon v2.0.
        :param momentum_buffer: Minimum price momentum buffer to delay confidence exit.
        """
        self.broker_client = broker_client
        self.confidence_floor = confidence_floor
        self.confidence_drop_threshold = confidence_drop_threshold
        self.hero_mode_close_time = hero_mode_close_time
        self.trail_to_moon_buffer = trail_to_moon_buffer
        self.momentum_buffer = momentum_buffer

    async def evaluate_trade(self, trade):
        """
        Evaluates open trade for exit conditions: TP/SL, Trail-to-Moon, confidence, Hero Mode.
        """
        current_price = await self.broker_client.get_price(trade['symbol'])

        # 1. TP/SL logic
        if await self._check_tp_sl(trade, current_price):
            return

        # 2. Trail-to-Moon v2.0
        if trade.get('forecast_tp'):
            await self._trail_to_moon(trade, current_price)

        # 3. Confidence-buffered exit with momentum delay
        if self._confidence_exit(trade, current_price):
            await self.broker_client.close_trade(trade['trade_id'], reason='confidence_exit')
            return

        # 4. Hero Mode early exit
        if self._hero_mode_exit(trade, current_price):
            await self.broker_client.close_trade(trade['trade_id'], reason='hero_mode_timeout')

    async def _check_tp_sl(self, trade, current_price):
        if trade['side'] == 'buy':
            if current_price >= trade['take_profit']:
                await self.broker_client.close_trade(trade['trade_id'], reason='take_profit')
                return True
            elif current_price <= trade['stop_loss']:
                await self.broker_client.close_trade(trade['trade_id'], reason='stop_loss')
                return True
        elif trade['side'] == 'sell':
            if current_price <= trade['take_profit']:
                await self.broker_client.close_trade(trade['trade_id'], reason='take_profit')
                return True
            elif current_price >= trade['stop_loss']:
                await self.broker_client.close_trade(trade['trade_id'], reason='stop_loss')
                return True
        return False

    async def _trail_to_moon(self, trade, current_price):
        forecast_tp = trade['forecast_tp']
        activation_price = forecast_tp * self.trail_to_moon_buffer

        if current_price >= activation_price:
            atr = trade.get('atr', 0.5)
            trail_distance = atr * 0.6
            await self._apply_trailing_stop(trade, current_price, trail_distance)

    async def _apply_trailing_stop(self, trade, current_price, trail_distance):
        if trade['side'] == 'buy':
            new_stop = current_price - trail_distance
            if new_stop > trade['stop_loss']:
                trade['stop_loss'] = new_stop
                await self.broker_client.update_trade(trade['trade_id'], trade)
        elif trade['side'] == 'sell':
            new_stop = current_price + trail_distance
            if new_stop < trade['stop_loss']:
                trade['stop_loss'] = new_stop
                await self.broker_client.update_trade(trade['trade_id'], trade)

    def _confidence_exit(self, trade, current_price):
        initial_confidence = trade.get('initial_confidence')
        current_confidence = trade.get('current_confidence')

        if initial_confidence and current_confidence:
            drop_pct = (initial_confidence - current_confidence) / initial_confidence
            below_floor = current_confidence < self.confidence_floor
            is_profitable = current_price > trade['entry_price'] if trade['side'] == 'buy' else current_price < trade['entry_price']

            # Delayed exit: if momentum is still positive, delay exit
            momentum_ok = self._check_price_momentum(trade, current_price)

            return (below_floor or drop_pct >= self.confidence_drop_threshold) and is_profitable and not momentum_ok
        return False

    def _check_price_momentum(self, trade, current_price):
        """
        Checks if price momentum is still favorable to delay exit.
        """
        last_prices = trade.get('recent_prices', [])
        if len(last_prices) < 3:
            return False

        momentum = (current_price - last_prices[-3]) / last_prices[-3]
        return momentum > self.momentum_buffer

    def _hero_mode_exit(self, trade, current_price):
        if trade.get('mode') == 'Hero':
            time_elapsed = (datetime.utcnow() - trade['entry_time']).total_seconds() / 60
            is_profitable = (current_price > trade['entry_price'] if trade['side'] == 'buy' else current_price < trade['entry_price'])
            return time_elapsed >= self.hero_mode_close_time and is_profitable
        return False
