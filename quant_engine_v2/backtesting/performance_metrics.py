import pandas as pd
import numpy as np

class PerformanceMetrics:
    def __init__(self):
        pass

    def calculate_metrics(self, trades):
        if not trades:
            return {}
            
        df = pd.DataFrame(trades)
        wins = df[df['pnl'] > 0]
        losses = df[df['pnl'] <= 0]
        
        total_pnl = df['pnl'].sum()
        win_rate = len(wins) / len(df) if len(df) > 0 else 0
        profit_factor = abs(wins['pnl'].sum() / losses['pnl'].sum()) if len(losses) > 0 and losses['pnl'].sum() != 0 else np.inf
        
        return {
            'total_trades': len(df),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_pnl': total_pnl,
            'avg_win': wins['pnl'].mean() if not wins.empty else 0,
            'avg_loss': losses['pnl'].mean() if not losses.empty else 0,
            'max_drawdown': self._calculate_drawdown(df['pnl'])
        }

    def _calculate_drawdown(self, pnl_series):
        cumulative = pnl_series.cumsum()
        peak = cumulative.expanding(min_periods=1).max()
        drawdown = (cumulative - peak)
        return drawdown.min()
