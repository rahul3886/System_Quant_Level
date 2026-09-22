# Structural Scoring Model

The engine uses a 110-point confluence system to validate signals.

## Matrix

| Component | Logic | Points |
|-----------|-------|--------|
| **Structure** | BOS in direction | +20 |
| | HH/HL Sequence | +10 |
| **Liquidity** | Sweep Detected | +15 |
| | Pool Sweep (3+ touches) | +10 |
| **Displacement**| Body > 1.2x ATR | +10 |
| | Volume Spike | +5 |
| | Imbalance (FVG) creation | +5 |
| **Zone** | In Demand/Supply | +10 |
| | Premium FVG Zone | +5 |
| **Regime** | Trending Strong | +15 |
| | Expansion Confirmed | +10 |
| | Compression | -30 (Blocker) |

## Thresholds

- **Trending Strong**: 60
- **Trending Weak**: 65
- **Expansion**: 70
- **Ranging**: 80
- **Compression**: Disabled
