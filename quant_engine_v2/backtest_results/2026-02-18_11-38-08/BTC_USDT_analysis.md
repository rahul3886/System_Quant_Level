# BTC/USDT Backtest Analysis (3-Day Sweep)

## Performance Matrix

| Threshold | TF | Trades | Win Rate | Profit Factor | Total PnL |
|-----------|----|--------|----------|---------------|-----------|
| 60 | 1m | 127 | 37.0% | 0.38 | -2332.93 |
| 70 | 1m | 50 | 42.0% | 0.51 | -740.07 |
| 80 | 1m | 11 | 45.4% | 1.92 | +178.33 |
| 60 | 5m | 145 | 53.1% | 1.05 | +200.39 |
| 70 | 5m | 47 | 46.8% | 1.28 | +326.26 |
| 80 | 5m | 7 | 71.4% | 8.11 | +348.28 |

## Insights

- **Optimal Setting**: 5m Timeframe @ 80 Threshold. This produced the highest Profit Factor (8.11) and Win Rate (71.4%), albeit with low trade frequency.
- **Threshold 60/70**: Generated too many signals on both 1m and 5m, resulting in poor risk-adjusted returns.
- **1m Noise**: Lower thresholds on 1m are catastrophic, suggesting that structural interpretation on 1m needs substantial HTF filtering.

## Suggested Upgrades

1. **Multi-Timeframe (MTF) Alignment**: Require 15m/1h Trend Persistence before a 1m/5m signal fires.
2. **Volume Profiling**: Add a "Value Area" filter. Only take long trades if price is below POC (Point of Control) in a bullish regime.
3. **Inducement Logic**: Filter out BOS that haven't swept a recent internal high/low (inducement) to avoid retail traps.
