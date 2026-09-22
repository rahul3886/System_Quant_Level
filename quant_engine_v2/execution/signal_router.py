class SignalRouter:
    def __init__(self):
        self.outputs = []

    def route_signal(self, signal_package):
        if signal_package['signal'] == "NEUTRAL":
            return
            
        print(f"📡 ROUTING SIGNAL: {signal_package['signal']} | Score: {signal_package['strength_score']} | Regime: {signal_package['regime']}")
        
        # In a real system, this would send to Telegram, Discord, or the LiveExecutor
        # For now, we log to console
        self._log_signal(signal_package)

    def _log_signal(self, pkg):
        import json
        with open("quant_engine_v2/logs/signal_history.jsonl", "a") as f:
            # Convert timestamp to string before serializing
            pkg_copy = pkg.copy()
            if 'timestamp' in pkg_copy:
                pkg_copy['timestamp'] = str(pkg_copy['timestamp'])
            f.write(json.dumps(pkg_copy) + "\n")
