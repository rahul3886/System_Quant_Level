# Live Demo Deployment Guide

This guide ensures you can deploy the Quant Engine v2 in Live Demo mode using the validated "Sweet Spot" configurations.

## 1. Prerequisites

- **Python Environment**: Ensure `pytz`, `tabulate`, and `requests` are installed.
- **Discord Webhook**: Have your Discord channel webhook URL ready.

## 2. Configuration

The assets are pre-configured in `quant_engine_v2/scripts/run_live_demo.py` based on our baseline sweep:

| Asset | TF | Threshold | Role |
| :--- | :--- | :--- | :--- |
| BTC/USDT | 5m | 80 | Institutional Breakout |
| SOL/USDT | 5m | 80 | Trend Expansion |
| BNB/USDT | 1m | 60 | Scalp Momentum |
| EURAUD | 1m | 80 | Asian Sniper |
| XAUUSD | 5m | 60 | Trend Monster |
| USDCHF | 1m | 80 | Low-Vol Breakout |

## 3. Launching the Session

To run the session and ensure all modules are found, use this command from the **root directory** (`C:\BILLIONAIRE RAHUL BOGI\System_Quant_Level`):

```powershell
$env:PYTHONPATH = "."
python quant_engine_v2/scripts/run_live_demo.py
```

*Note: I have also added an automatic path-fix inside the script, so it should now work even if you run it directly from VS Code or by clicking 'Run'.*

## 4. Customizing Assets/Thresholds

To add a new asset or change a threshold:

1. Open `quant_engine_v2/scripts/run_live_demo.py`.
2. Locate the `ASSETS_TO_TRADE` list.
3. Add a new dictionary entry:

   ```python
   {'symbol': 'ETH/USDT', 'tf': '5m', 'threshold': 85},
   ```

## 5. Monitoring

- **Terminal**: A live formatted table will print every time a trade is detected.
- **Logs**: Detailed markdown logs are saved to `quant_engine_v2/logs/live_demo_session.md`.
- **Discord**: Real-time alerts will be sent to your configured channel with signal reasoning and geometry.

---
**Note**: Investment is set to **$10,000** per trade. This can be adjusted in the `INVESTMENT_PER_TRADE` variable in the script.
