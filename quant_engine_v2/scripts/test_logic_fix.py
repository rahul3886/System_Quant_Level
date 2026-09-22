import sys
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, project_root)

from quant_engine_v2.core.v1.scoring_engine import ScoringEngine

def test_sl_tp_logic():
    engine = ScoringEngine()
    
    # Mock data for a BEARISH structure where price is below a recent high (swing high)
    # and has a lower swing low.
    structure_info = {
        'last_bos': 'BEARISH',
        'trend_direction': -1,
        'structure_state': 'LL_LH',
        'structural_targets': {
            'liquidity_high': 620.0, # Recent peak (Stop Loss for SELL)
            'liquidity_low': 610.0   # Recent trough (Take Profit for SELL)
        }
    }
    
    regime_info = {
        'regime': 'TRENDING_STRONG',
        'price': 615.0 # Entry price
    }
    
    liquidity_info = {'sweep_detected': 'BSL_SWEEP', 'pool_sweep': False}
    displacement_info = {'displacement_score': 10, 'imbalance_zones': True}

    print("--- TESTING SELL SIGNAL TARGETS ---")
    result = engine.score_signal(regime_info, structure_info, liquidity_info, displacement_info, threshold_override=50)
    
    print(f"Signal: {result['signal']}")
    print(f"Entry Price: {regime_info['price']}")
    print(f"Stop Loss: {result['structural_sl']}")
    print(f"Take Profit: {result['structural_tp']}")
    
    # Validation
    if result['signal'] == 'SELL':
        if result['structural_tp'] < regime_info['price']:
            print("✅ SUCCESS: Take Profit is below entry price for SELL.")
        else:
            print("❌ FAILURE: Take Profit is above entry price for SELL.")
            
        if result['structural_sl'] > regime_info['price']:
            print("✅ SUCCESS: Stop Loss is above entry price for SELL.")
        else:
            print("❌ FAILURE: Stop Loss is below entry price for SELL.")

if __name__ == "__main__":
    test_sl_tp_logic()
