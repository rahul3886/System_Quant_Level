import os
import sys
import time
import pandas as pd
from datetime import datetime
import pytz

# Add project root to sys.path to resolve 'quant_engine_v2' module
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.core.v1.signal_engine import SignalEngine
from quant_engine_v2.utils.discord_notifier import DiscordNotifier

# --- CONFIGURATION ---
ASSETS_TO_TRADE = [
    {'symbol': 'BTC/USDT', 'tf': '5m', 'threshold': 60},
    {'symbol': 'SOL/USDT', 'tf': '5m', 'threshold': 60},
    {'symbol': 'BNB/USDT', 'tf': '1m', 'threshold': 60},
    {'symbol': 'EURAUD', 'tf': '1m', 'threshold': 60},
    {'symbol': 'XAUUSD', 'tf': '5m', 'threshold': 60},
    {'symbol': 'USDCHF', 'tf': '1m', 'threshold': 60},
]

INVESTMENT_PER_TRADE = 10000
IST = pytz.timezone('Asia/Kolkata')
# Create timestamped log file for each session
SESSION_START = datetime.now(IST).strftime("%Y%m%d_%H%M")
LOG_FILE = os.path.join(project_root, "quant_engine_v2", "logs", f"session_{SESSION_START}.md")
MASTER_LOG = os.path.join(project_root, "quant_engine_v2", "logs", "live_demo_session.md")

console = Console()

class LiveDemoSession:
    def __init__(self):
        self.data_provider = DataProvider()
        self.signal_engine = SignalEngine()
        self.notifier = DiscordNotifier()
        self.trades = []
        # Unique tracking: (symbol, tf, threshold)
        self.last_processed_ts = {}
        self.active_positions = {}
        self._init_log()

    def _init_log(self):
        console.print(f"[bold cyan]DEBUG: Initializing logging system...[/bold cyan]")
        console.print(f"DEBUG: LOG_FILE = {LOG_FILE}")
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        # Always initialize fresh session log
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# 📈 LIVE SESSION LOG: {SESSION_START}\n\n")
            f.write(f"> **Started**: {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')} IST\n")
            f.write("> **Status**: Active | **Position Size**: $10,000\n\n")
            f.write("> **Institutional Mode**: Multi-Timeframe Draw on Liquidity targets enabled.\n\n")
            self._write_table_header(f)
        console.print(f"[bold green]DEBUG: Session log created: {LOG_FILE}[/bold green]")
        
        # Ensure master log exists
        if not os.path.exists(MASTER_LOG):
            with open(MASTER_LOG, 'w', encoding='utf-8') as f:
                f.write("# 📈 MASTER LIVE DEMO SESSION LOGS\n\n")
                self._write_table_header(f)

    def _write_table_header(self, f):
        f.write("| Session | Time (IST) | Event | Asset | TF | Thresh | Side | Price | SL | TP | ROI % | Score | Details |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")

    def get_session_name(self, dt_ist):
        hour = dt_ist.hour
        if 5 <= hour < 14: return "ASIAN"
        if 14 <= hour < 21: return "LONDON"
        return "NEW_YORK"

    def log_trade_markdown(self, row_data):
        try:
            # Clean row data of pipe characters to avoid MD breakage
            cleaned_row = [str(x).replace("|", "/") for x in row_data]
            line = f"| {' | '.join(cleaned_row)} |\n"
            # Write to session log
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(line)
                f.flush()
                os.fsync(f.fileno())
            # Write to master log
            with open(MASTER_LOG, 'a', encoding='utf-8') as f:
                f.write(line)
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            console.print(f"[red]FAILED TO WRITE LOG: {e}[/red]")

    def create_dashboard_table(self):
        table = Table(title="💎 LIVE TRADING DASHBOARD (IST)", title_style="bold magenta", expand=True)
        table.add_column("Session", style="cyan")
        table.add_column("Time", style="white")
        table.add_column("Asset", style="bold yellow")
        table.add_column("TF", style="dim")
        table.add_column("Thresh", style="dim")
        table.add_column("Side", style="bold green")
        table.add_column("Price", justify="right")
        table.add_column("Score", justify="center", style="bold blue")
        table.add_column("Status", style="italic")

        for t in self.trades[-10:]:
            table.add_row(
                t['session'], t['time'], t['symbol'], t['tf'], str(t['threshold']),
                t['side'], f"{t['price']:.5f}", str(t['score']), "[green]EXECUTED[/green]"
            )
        return table

    def run(self):
        with Live(self.create_dashboard_table(), console=console, refresh_per_second=1) as live:
            console.print(Panel("[bold green]SESSION INITIALIZED[/bold green] - Monitoring with Smart MTF Targets..."))
            
            while True:
                now_ist = datetime.now(IST)
                live.update(Panel(self.create_dashboard_table(), title=f"SCANNING | Assets: {len(ASSETS_TO_TRADE)} | {now_ist.strftime('%H:%M:%S')}", border_style="green"))
                
                for asset in ASSETS_TO_TRADE:
                    key = f"{asset['symbol']}_{asset['tf']}_{asset['threshold']}"
                    try:
                        df = self.data_provider.get_data(asset['symbol'], asset['tf'], limit=100)
                        if df.empty: continue
                        
                        htf_df = None
                        if asset['tf'] == '1m':
                            htf_df = self.data_provider.get_data(asset['symbol'], '5m', limit=100)
                        
                        # Exit Monitoring
                        active_pos = self.active_positions.get(key)
                        current_price = df['close'].iloc[-1]
                        
                        if active_pos:
                            exit_triggered = False
                            reason = ""
                            pnl = 0
                            
                            tp = active_pos.get('tp', 0)
                            sl = active_pos.get('sl', 0)
                            
                            if active_pos['side'] == "BUY":
                                if current_price >= tp and tp > 0: exit_triggered, reason = True, "TP HIT"
                                elif current_price <= sl and sl > 0: exit_triggered, reason = True, "SL HIT"
                            else:
                                if current_price <= tp and tp > 0: exit_triggered, reason = True, "TP HIT"
                                elif current_price >= sl and sl > 0: exit_triggered, reason = True, "SL HIT"
                                
                            if exit_triggered:
                                if active_pos['side'] == "BUY":
                                    pnl = ((current_price - active_pos['entry']) / active_pos['entry']) * 100
                                else:
                                    pnl = ((active_pos['entry'] - current_price) / active_pos['entry']) * 100
                                
                                self.log_trade_markdown([
                                    self.get_session_name(now_ist), now_ist.strftime("%H:%M:%S"), reason,
                                    asset['symbol'], asset['tf'], asset['threshold'], active_pos['side'],
                                    f"{current_price:.5f}", "---", "---", f"{pnl:.2f}%", 
                                    active_pos.get('score', 0), f"Exit @ {current_price:.5f}"
                                ])
                                self.notifier.send_system_update(f"🎯 **EXIT: {asset['symbol']}** | {reason} ({pnl:.2f}%)")
                                self.active_positions[key] = None
                                continue

                        # Signal Detection
                        signal_pkg = self.signal_engine.generate_signal(df, htf_df=htf_df, threshold_override=asset['threshold'])
                        
                        if signal_pkg and signal_pkg['signal'] != "NEUTRAL":
                            ts = str(signal_pkg['timestamp'])
                            if ts != self.last_processed_ts.get(key):
                                self.last_processed_ts[key] = ts
                                
                                sl_val = signal_pkg.get('structural_sl') or 0
                                tp_val = signal_pkg.get('structural_tp') or 0
                                
                                self.active_positions[key] = {
                                    'side': signal_pkg['signal'], 'entry': signal_pkg['price'],
                                    'sl': sl_val, 'tp': tp_val, 'score': signal_pkg.get('score', 0)
                                }
                                
                                trade_entry = {
                                    'session': self.get_session_name(now_ist), 'time': now_ist.strftime("%H:%M:%S"),
                                    'symbol': asset['symbol'], 'tf': asset['tf'], 'threshold': asset['threshold'],
                                    'side': signal_pkg['signal'], 'price': signal_pkg['price'], 'score': signal_pkg.get('score', 0)
                                }
                                self.trades.append(trade_entry)
                                
                                self.log_trade_markdown([
                                    trade_entry['session'], now_ist.strftime("%Y-%m-%d %H:%M:%S"), "ENTRY",
                                    asset['symbol'], asset['tf'], asset['threshold'], trade_entry['side'],
                                    f"{trade_entry['price']:.5f}", f"{sl_val:.5f}", f"{tp_val:.5f}",
                                    "0.00%", trade_entry['score'], signal_pkg.get('reasoning', '')[:50]
                                ])
                                
                                self.notifier.send_trade({
                                    'asset': asset['symbol'], 'tf': asset['tf'], 'threshold': asset['threshold'],
                                    'signal': signal_pkg['signal'], 'price': signal_pkg['price'],
                                    'sl': sl_val, 'tp': tp_val, 'score': signal_pkg.get('score', 0),
                                    'reason': signal_pkg.get('reasoning', ''),
                                    'geometry': f"📊 Regime: {signal_pkg.get('regime', 'N/A')} | 🏗️ Structure: {signal_pkg.get('structure', 'N/A')}",
                                    'time_ist': now_ist.strftime("%Y-%m-%d %H:%M:%S")
                                })
                    except Exception as e:
                        import traceback
                        console.print(f"[red]Error on {key}: {e}[/red]")
                        traceback.print_exc()

                time.sleep(10)

if __name__ == "__main__":
    session = LiveDemoSession()
    session.run()
