# XAUUSD Backtest Analysis (3-Day Sweep)

## Performance Matrix

| Threshold | TF | Trades | Win Rate | Profit Factor | Total PnL |
|-----------|----|--------|----------|---------------|-----------|
| 60 | 1m | 377 | 43.5% | 0.61 | -3307.38 |
| 70 | 1m | 121 | 46.2% | 0.74 | -1484.56 |
| 80 | 1m | 16 | 43.7% | 0.49 | -329.00 |
| 60 | 5m | 114 | 43.8% | 3.57 | +11006.92 |
| 70 | 5m | 32 | 31.2% | 1.75 | +1032.85 |

## Insights

- **PnL Outlier**: XAUUSD 5m @ 60 threshold produced +$11,000 PnL. This suggests a massive trending move where the system captured large R-multiples, despite a 43% win rate.
- **Volatility Scaling**: Gold's high ATR means position sizing must be strictly scaled to avoid the high drawdowns observed (-5k peak).

## Suggested Upgrades

1. **Risk-to-Reward (RR) Threshold**: Enforce a minimum 1:2.5 RR before firing.
2. **Volatility Guard**: If ATR(14) is in the 90th percentile, reduce position size by 75% instead of 50%.
3. **Liquidity Sweep Depth**: Require price to sweep at least 2 pips beyond the SSL/BSL cluster for metals to confirm a genuine sweep.
