# Regime-Adaptive Structural Trading Engine (v2)

## System Architecture

The system is designed as a modular pipeline for market interpretation and trade execution.

### Components

1. **Structure Engine**: Detects swing highs/lows and maps BOS/CHoCH to establish market bias.
2. **Regime Engine**: Classifies market conditions (Trending Strong, Compression, etc.) using trend persistence and volatility metrics.
3. **Liquidity Engine**: Identifies SSL/BSL pools and detects sweeps as high-probability triggers.
4. **Displacement Engine**: Confirms institutional footprints using ATR-based body expansion and FVG identification.
5. **Scoring Engine**: Confluence-based signal validator with dynamic thresholds based on the current regime.
6. **Risk Engine**: Adjusts position sizes and risk parameters dynamically across regimes.

## Data Flow

`DataProvider` -> `SignalEngine` (Structure -> Liquidity -> Displacement -> Regime) -> `ScoringEngine` -> `SignalRouter` -> `LiveExecutor` | `BacktestEngine`
