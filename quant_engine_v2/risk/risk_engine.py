from quant_engine_v2.configs.regime_config import REGIMES

class RiskEngine:
    def __init__(self, base_risk_per_trade=0.01):
        self.base_risk = base_risk_per_trade

    def calculate_adjusted_risk(self, regime):
        multiplier = REGIMES.get(regime, {}).get('risk_multiplier', 1.0)
        return self.base_risk * multiplier

    def apply_volatility_scaling(self, risk_amount, volatility_state):
        if volatility_state == "HIGH_VOL":
            return risk_amount * 0.5 # Half risk if vol is extremely high
        return risk_amount
