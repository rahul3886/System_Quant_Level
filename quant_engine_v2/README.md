# Quant Engine v2

A compact overview and run instructions for the Quant Engine v2 project (algorithmic backtesting and execution framework).

## Overview

- **Purpose:** A modular engine for building, backtesting, and (optionally) running live algorithmic trading strategies. It provides data ingestion, signal generation, regime detection, scoring, risk sizing, execution routing, and backtesting utilities.
- **Key folders:**
  - `core/` — core engines (signal, regime, scoring, liquidity, structure, displacement).
  - `backtesting/` — backtest engine and performance metrics.
  - `configs/` — asset, regime and tuning configs.
  - `data/` — data provider and data utilities.
  - `execution/` — live executor and signal router.
  - `risk/` — position sizing and risk engine.
  - `scripts/` — convenience scripts for running backtests, sweeps, demo runs and analysis.
  - `backtest_results/` — stores generated backtest outputs and analysis reports.

## Quick Start (local)

1. Install Python (recommended 3.10+).
2. Create and activate a virtual environment:

   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows CMD:
     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```

3. Install dependencies (if a `requirements.txt` exists):

   ```bash
   pip install -r requirements.txt
   ```

   If the repo does not include `requirements.txt`, install common data and numeric packages typically required by quant projects: `numpy`, `pandas`, `scipy`, `matplotlib`. Add `ta-lib`, `ccxt`, or other packages as needed by your strategies.

4. Run the project entrypoint for a quick look:

   From the repository root (where this README sits):

   ```bash
   python main.py
   ```

   `main.py` is a good starting point to see example runs; open it to inspect what it executes and which configs it uses.

## Useful Scripts

- `scripts/run_backtest.py` — single backtest runner.
- `scripts/run_backtest_sweep.py` — parameter sweep/backtest grid search; outputs into `backtest_results/`.
- `scripts/run_live_demo.py` — demo of live-execution flow (if configured/environment connected).
- `scripts/analyze_backtest.py` — generate analysis reports from results in `backtest_results/`.

Run any script from the repository root, for example:

```bash
python scripts/run_backtest.py
python scripts/run_backtest_sweep.py
python scripts/run_live_demo.py
python scripts/analyze_backtest.py
```

Note: Each script may accept command-line arguments. Open the script header to view usage and available options.

## Configuration

- `configs/asset_config.py` and `configs/regime_config.py` contain key strategy and asset parameters. Edit or create config variants to run different experiments.
- `configs/sweet_spots.py` holds tuned parameter ranges used by sweep scripts.

## Data

- The `data/` package contains a data provider abstraction. Place local market data in a structure expected by the provider or adapt the provider to your data source.
- Example analysis inputs/outputs can be found under `analysis_temp/` and `backtest_results/`.

## Backtest Results & Analysis

- Backtest runs create subfolders under `backtest_results/` using timestamps. Each run may include per-asset folders and CSV summaries (e.g. `sweep_summary.csv`) and Markdown analysis files (e.g. `BTC_USDT_analysis.md`).

## Running a Minimal Backtest (recommended first step)

1. Inspect `scripts/run_backtest.py` to understand required arguments or default behavior.
2. Prepare a config in `configs/` if needed.
3. Run:

```bash
python scripts/run_backtest.py
```

4. View outputs in `backtest_results/` and open generated analysis markdown files.

## Live / Execution

- The `execution/` package contains `live_executor.py` and `signal_router.py`. These components require external connectivity (broker/exchange) and careful testing. Use `run_live_demo.py` to exercise the live flow in a simulated/demo environment before connecting real accounts.

## Development Tips

- Start by reading `main.py` and scripts under `scripts/` to discover entry points.
- Use small, reproducible backtests when tuning a new signal or regime model.
- Keep config variants in `configs/` and record runs by copying configs into `backtest_results/<run>/` for reproducibility.

## Next Steps / How I can help

- I can: create a `requirements.txt`, run a sample backtest, or add a short example script that executes a minimal backtest and prints a perf summary. Tell me which you'd like.

---

File: quant_engine_v2/README.md
