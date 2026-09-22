from quant_engine_v2.configs.regime_config import REGIMES

class ScoringEngine:
    def __init__(self):
        pass

    def score_signal(self, regime_info, structure_info, liquidity_info, displacement_info, threshold_override=None):
        score = 0
        regime = regime_info['regime']
        
        # 1. Structure Alignment (0–30)
        if structure_info['last_bos'] == ("BULLISH" if structure_info['trend_direction'] == 1 else "BEARISH"):
            score += 20
        if "HH_HL" in structure_info['structure_state'] or "LL_LH" in structure_info['structure_state']:
            score += 10
            
        # 2. Liquidity Event (0–25)
        if liquidity_info['sweep_detected']:
            score += 15
        if liquidity_info['pool_sweep']:
            score += 10
            
        # 3. Displacement (0–20)
        score += displacement_info['displacement_score']
        
        # 4. Zone Confluence (0–15)
        # Simplified: if price is in a recently created FVG zone
        if displacement_info['imbalance_zones']:
            score += 10 # In Demand/Supply (Demand if bullish, Supply if bearish)
            
        # 5. Regime Alignment (0–20)
        if regime == 'TRENDING_STRONG':
            score += 15
        elif regime == 'EXPANSION':
            score += 10
        elif regime == 'COMPRESSION':
            score -= 30
            
        # Dynamic Threshold Selection
        threshold = threshold_override if threshold_override is not None else REGIMES.get(regime, {}).get('threshold', 70)
        
        signal = "NEUTRAL"
        if regime != 'COMPRESSION':
            if score >= threshold:
                signal = "BUY" if structure_info['trend_direction'] == 1 else "SELL"
                if structure_info['trend_direction'] == 0:
                     # If no clear trend but sweep detected, use sweep direction
                     if liquidity_info['sweep_detected'] == "SSL_SWEEP": signal = "BUY"
                     if liquidity_info['sweep_detected'] == "BSL_SWEEP": signal = "SELL"

        # Structural SL/TP Generation
        sl = structure_info['structural_targets']['sl']
        tp = structure_info['structural_targets']['tp']
        
        # Structural RR calculation
        rr = 0
        if sl and tp:
             # Basic RR: (TP - Entry) / (Entry - SL)
             # Entry approximated as current close
             pass

        return {
            'signal': signal,
            'strength_score': score,
            'threshold': threshold,
            'structural_sl': sl,
            'structural_tp': tp,
            'regime_penalty_boost': REGIMES.get(regime, {}).get('boost', 0)
        }
