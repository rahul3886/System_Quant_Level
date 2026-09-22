import sys
import os
import pytz
from datetime import datetime

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, project_root)

from quant_engine_v2.utils.discord_notifier import DiscordNotifier

def test_full_pipeline():
    notifier = DiscordNotifier()
    
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    
    print("Testing Discord...")
    notifier.send_system_update(f"🛠️ DEEP ANALYSIS TEST: Manual check at {now} IST.")
    
    notifier.send_trade({
        'asset': 'TEST/SIGNAL',
        'tf': '1m',
        'threshold': 'DEBUG',
        'signal': 'BUY',
        'price': 123.456,
        'sl': 120.0,
        'tp': 130.0,
        'score': 100,
        'reason': "DEEP ANALYSIS: Verifying if alerts fire after 'reasoning' fix.",
        'geometry': '📊 Regime: STABLE | 🏗️ Structure: TEST',
        'time_ist': now
    })
    print("Done.")

if __name__ == "__main__":
    test_full_pipeline()
