# Regime Detection Model

The system mathematically defines 5 primary market regimes.

## 1. Trend Persistence

- **Bullish**: `(HH count + HL count) - (LH count + LL count) > 3`
- **Bearish**: `(HH count + HL count) - (LH count + LL count) < -3`

## 2. Volatility State

- **High Vol**: > 75th Percentile
- **Low Vol**: < 25th Percentile

## 3. Compression

- Logic: `Range (20) / ATR (20) < 1.5`
- Characterized by tight consolidation and low volatility.

## 4. Expansion

- Logic: `Displacement Count (last 15) > 3`
- Characterized by aggressive candles and FVG creation.

## 5. Ranging

- Default state when trend persistence is weak and no clear expansion/compression is detected.
