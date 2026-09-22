# Import will be dynamic in __init__
# from quant_engine_v2.core.signal_engine import SignalEngine
from quant_engine_v2.risk.risk_engine import RiskEngine
from quant_engine_v2.risk.position_sizing import PositionSizer
from quant_engine_v2.backtesting.performance_metrics import PerformanceMetrics

class BacktestEngine:
    def __init__(self, initial_balance=10000, version=None):
        if version == 'v1':
            from quant_engine_v2.core.v1.signal_engine import SignalEngine
        else:
            from quant_engine_v2.core.signal_engine import SignalEngine
            
        self.signal_engine = SignalEngine()
        self.risk_engine = RiskEngine()
        self.sizer = PositionSizer(initial_balance)
        self.metrics = PerformanceMetrics()
        self.trades = []

    def run(self, df, threshold_override=None):
        print(f"🔄 STARTING BACKTEST | Data Points: {len(df)} | Threshold: {threshold_override}")
        
        # Using a rolling window to simulate live signal generation
        window_size = 50
        for i in range(window_size, len(df)):
            window_df = df.iloc[i-window_size:i]
            signal_pkg = self.signal_engine.generate_signal(window_df, threshold_override=threshold_override)
            
            if signal_pkg and signal_pkg['signal'] != "NEUTRAL":
                self._process_signal(signal_pkg, df.iloc[i])

        metrics = self.metrics.calculate_metrics(self.trades)
        return {
            'metrics': metrics,
            'trades': self.trades
        }

    def _process_signal(self, pkg, next_candle):
        entry = pkg['price']
        sl = pkg['structural_sl']
        tp = pkg['structural_tp']
        
        if not sl or not tp:
             # Default SL/TP if structural detection failed
             sl = entry * 0.99 if pkg['signal'] == "BUY" else entry * 1.01
             tp = entry * 1.02 if pkg['signal'] == "BUY" else entry * 0.98

        risk_pct = self.risk_engine.calculate_adjusted_risk(pkg['regime'])
        size = self.sizer.calculate_size(risk_pct, entry, sl)
        
        if size == 0: return

        # Simple outcome simulation (look ahead to next candle)
        # In a real backtest, we'd walk forward until sl or tp hit
        pnl = 0
        if pkg['signal'] == "BUY":
            pnl = (next_candle['close'] - entry) * size
        else:
            pnl = (entry - next_candle['close']) * size
            
        self.trades.append({
            'timestamp': pkg['timestamp'],
            'signal': pkg['signal'],
            'entry': entry,
            'pnl': pnl,
            'regime': pkg['regime']
        })
        
        self.sizer.update_balance(self.sizer.balance + pnl)
