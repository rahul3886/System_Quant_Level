from quant_engine_v2.core.structure_engine import StructureEngine
from quant_engine_v2.core.regime_engine import RegimeEngine
from quant_engine_v2.core.liquidity_engine import LiquidityEngine
from quant_engine_v2.core.displacement_engine import DisplacementEngine
from quant_engine_v2.core.scoring_engine import ScoringEngine

class SignalEngine:
    def __init__(self):
        self.structure = StructureEngine()
        self.regime = RegimeEngine()
        self.liquidity = LiquidityEngine()
        self.displacement = DisplacementEngine()
        self.scoring = ScoringEngine()

    def generate_signal(self, df, threshold_override=None):
        if df.empty or len(df) < 50:
            return None
            
        # 1. Structural Interpretation
        structure_info = self.structure.get_structure_data(df)
        
        # 2. Regime Detection
        regime_info = self.regime.calculate_regime(df, structure_info)
        
        # 3. Liquidity Identification
        liquidity_info = self.liquidity.detect_liquidity(df)
        
        # 4. Displacement Confirmation
        displacement_info = self.displacement.detect_displacement(df)
        
        # 5. Final Scoring
        final_signal = self.scoring.score_signal(
            regime_info, 
            structure_info, 
            liquidity_info, 
            displacement_info,
            threshold_override=threshold_override
        )
        
        # Combine all data for reporting
        return {
            'timestamp': df['timestamp'].iloc[-1],
            'price': df['close'].iloc[-1],
            **final_signal,
            'regime': regime_info['regime'],
            'structure': structure_info['structure_state'],
            'displacement_detected': displacement_info['displacement_detected'],
            'sweep_detected': liquidity_info['sweep_detected']
        }
