# Deep Trade Analysis & Upgrade Strategy

## 1. BTC/USDT 5m (Threshold 80) - High Yield Setup

- **Win Rate**: 71.43%
- **Profit Factor**: 8.11
- **Analysis**:
  - Performance is skewed towards **SELL** signals which captured 100% of the profit in the analyzed window.
  - Average win ($79.45) is significantly larger than average loss ($24.48), providing a robust risk cushion.
  - Max drawdown preserved within 5% of the total profit.

## 2. Live Demo Analysis Capabilities

- I have implemented `scripts/analyze_live.py` which extracts signal frequency and regime reliability from the live `signal_history.jsonl` log.
- This allows for real-time monitoring of whether the "Strong Trending" regime is actually yielding trades as expected.

## 3. High-Yield Preservation Logic

- **"The Vault"**: I have created `configs/sweet_spots.py` to store hardcoded thresholds for proven setups.
- **Dedicated Scripts**: `scripts/run_high_yield_btc.py` and `scripts/run_high_yield_xau.py` are now decoupled from the main engine loop, allowing you to run them even if the general engine logic undergoes aggressive experimentation.

## 4. Suggested Logic Upgrades (Step-by-Step)

### Step 1: MTF Strength Filter

- **Problem**: Lower timeframes (1m) are generating noise-induced BOS.
- **Solution**: Before a 5m signal fires, the **1h Regime** must NOT be `COMPRESSION`.

### Step 2: Inducement Identification

- **Problem**: Sweeps are sometimes just retail stop-runs that continue trending against us.
- **Solution**: Implement a "Confirmation Candle" rule—the price must close back inside the structural range within 3 candles of the sweep.

### Step 3: Volatility-Based TP Scaling

- **Problem**: Fixed structural targets are hit too slowly in `LOW_VOL` regimes.
- **Solution**: Scale TP to 1.5x ATR if the regime is `TRENDING_WEAK` to lock in profit faster.

## 5. Next Steps

- [ ] Run the `run_high_yield_xau.py` to verify Gold performance.
- [ ] Begin implementing **Step 1: MTF Strength Filter**.
