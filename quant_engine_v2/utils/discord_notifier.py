import requests
import json
from datetime import datetime

class DiscordNotifier:
    def __init__(self, webhook_url=None):
        # Using the user-provided webhook URL
        self.webhook_url = webhook_url or "https://discord.com/api/webhooks/1473640604582805627/UHxS8wkHrSOAFR8fvBw5ICPIasx3a8prZg9ZqSi7VR2H1u097nWUC0Hu3Z8V1jBpu1v_"

    def send_trade(self, trade_data):
        """
        Sends a formatted trade alert to Discord.
        trade_data: dict with asset, tf, threshold, signal, price, sl, tp, score, reason, geometry
        """
        if not self.webhook_url or "YOUR_DISCORD_WEBHOOK" in self.webhook_url:
            print("⚠️ Discord Webhook not configured. Skipping notification.")
            return

        embed = {
            "title": f"🚀 NEW TRADE: {trade_data['asset']} ({trade_data['signal']})",
            "color": 3066993 if trade_data['signal'] == "BUY" else 15158332,
            "fields": [
                {"name": "Price", "value": f"`{trade_data['price']}`", "inline": True},
                {"name": "TF", "value": f"`{trade_data['tf']}`", "inline": True},
                {"name": "Threshold", "value": f"`{trade_data['threshold']}`", "inline": True},
                {"name": "SL / TP", "value": f"`{trade_data['sl']}` / `{trade_data['tp']}`", "inline": True},
                {"name": "Score", "value": f"**{trade_data['score']}/110**", "inline": True},
                {"name": "Geometry", "value": f"```{trade_data['geometry']}```", "inline": False},
                {"name": "Reasoning", "value": trade_data['reason'], "inline": False},
                {"name": "Time (IST)", "value": trade_data['time_ist'], "inline": True}
            ],
            "footer": {"text": "System Quant Level v2 | Institutional Logic"}
        }

        payload = {"embeds": [embed]}
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            if response.status_code != 204:
                print(f"❌ Discord Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Discord Notify Failed: {e}")

    def send_system_update(self, message):
        if not self.webhook_url or "YOUR_DISCORD_WEBHOOK" in self.webhook_url: return
        payload = {"content": f"🔔 **SYSTEM UPDATE**: {message}"}
        requests.post(self.webhook_url, json=payload)
