# EURUSD Backtest Analysis (3-Day Sweep)

## Performance Matrix

| Threshold | TF | Trades | Win Rate | Profit Factor | Total PnL |
|-----------|----|--------|----------|---------------|-----------|
| 60 | 1m | 76 | 47.3% | 0.40 | -1574.20 |
| 70 | 1m | 27 | 51.8% | 0.22 | -1497.39 |
| 80 | 1m | 2 | 100.0% | inf | +12.18 |
| 60 | 5m | 37 | 27.0% | 0.19 | -2213.60 |

## Insights

- **General Failure**: The current logic failed significantly on EURUSD during this 3-day window. Low win rates on 5m (27%) suggest the "Regime" detection might have misclassified a ranging market as trending.
- **Spread Sensitivity**: 1m trades had high frequency but very poor outcome, likely due to structural targets being too close relative to ATR and spread.

## Suggested Upgrades

1. **Asian Range Filter**: Do not take EURUSD trades during the Asian session. Wait for London open liquidity sweeps.
2. **Session Persistence**: Only trade if Volume is > 1.2x of the 20-period average (London/NY overlap).
3. **Regime Penalty adjustment**: Increase the penalty for "RANGING" regimes from -0 to -15 in the scoring engine.
