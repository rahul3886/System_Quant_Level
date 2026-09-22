from quant_engine_v2.core.v1.structure_engine import StructureEngine
from quant_engine_v2.core.v1.regime_engine import RegimeEngine
from quant_engine_v2.core.v1.liquidity_engine import LiquidityEngine
from quant_engine_v2.core.v1.displacement_engine import DisplacementEngine
from quant_engine_v2.core.v1.scoring_engine import ScoringEngine

class SignalEngine:
    def __init__(self):
        self.structure = StructureEngine()
        self.regime = RegimeEngine()
        self.liquidity = LiquidityEngine()
        self.displacement = DisplacementEngine()
        self.scoring = ScoringEngine()

    def generate_signal(self, df, htf_df=None, threshold_override=None):
        if df.empty or len(df) < 50:
            return None
            
        # 1. Structural Interpretation
        structure_info = self.structure.get_structure_data(df)
        
        # 2. HTF Context (Draw on Liquidity)
        htf_structure = None
        if htf_df is not None and not htf_df.empty:
            htf_structure = self.structure.get_structure_data(htf_df)
        
        # 3. Regime Detection
        regime_info = self.regime.calculate_regime(df, structure_info)
        
        # 4. Liquidity Identification
        liquidity_info = self.liquidity.detect_liquidity(df)
        
        # 5. Displacement Confirmation
        displacement_info = self.displacement.detect_displacement(df)
        
        # 6. Final Scoring with HTF Priority
        current_price = df['close'].iloc[-1]
        final_signal = self.scoring.score_signal(
            regime_info, 
            structure_info, 
            liquidity_info, 
            displacement_info,
            current_price,
            threshold_override=threshold_override,
            htf_targets=htf_structure
        )
        
        # Combine all data for reporting (Ensure scoring targets overwrite structure targets)
        signal_data = {
            'timestamp': df['timestamp'].iloc[-1],
            'price': df['close'].iloc[-1],
            'regime': regime_info['regime'],
            'structure': structure_info['structure_state'],
            'displacement_detected': displacement_info['displacement_detected'],
            'sweep_detected': liquidity_info['sweep_detected']
        }
        signal_data.update(final_signal)
        return signal_data
