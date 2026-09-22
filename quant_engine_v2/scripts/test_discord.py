import sys
import os
# Add project root to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from quant_engine_v2.utils.discord_notifier import DiscordNotifier
from datetime import datetime
import pytz

notifier = DiscordNotifier()
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

test_trade = {
    'asset': 'TEST/SIGNAL',
    'signal': 'BUY',
    'price': 1.23456,
    'sl': 1.23000,
    'tp': 1.25000,
    'score': 110,
    'reason': '🔄 PROVING CONNECTION: This is a manual test signal to verify Discord is active.',
    'geometry': '📊 Regime: BULLISH_PULSE | 🏗️ Structure: BOS_DETECTED',
    'time_ist': now_ist
}

print("🚀 Sending test trade to Discord...")
notifier.send_trade(test_trade)
print("✅ Test complete.")
