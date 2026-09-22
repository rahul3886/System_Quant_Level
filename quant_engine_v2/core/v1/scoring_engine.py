from quant_engine_v2.configs.regime_config import REGIMES

class ScoringEngine:
    def __init__(self):
        pass

    def score_signal(self, regime_info, structure_info, liquidity_info, displacement_info, current_price, threshold_override=None, htf_targets=None):
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

        # Structural SL/TP Generation (Priority: HTF > LTF)
        # Smart Target Logic
        # Priority: HTF Swing Lists > LTF Swing Lists
        source = htf_targets if htf_targets else structure_info
        peaks = source.get('swing_highs', [])
        troughs = source.get('swing_lows', [])
        
        sl = None
        tp = None
        
        if signal == "BUY":
            # TP: Highest swing high above current price
            valid_tps = [h for h in peaks if h > current_price * 1.0005] # 0.05% room
            tp = max(valid_tps) if valid_tps else (current_price * 1.01) # fallback 1%
            
            # SL: Lowest recent trough below current price
            valid_sls = [l for l in troughs if l < current_price * 0.9995]
            sl = min(valid_sls) if valid_sls else (current_price * 0.99) # fallback 1%
            
        elif signal == "SELL":
            # TP: Lowest swing low below current price
            valid_tps = [l for l in troughs if l < current_price * 0.9995]
            tp = min(valid_tps) if valid_tps else (current_price * 0.99)
            
            # SL: Highest recent peak above current price
            valid_sls = [h for h in peaks if h > current_price * 1.0005]
            sl = max(valid_sls) if valid_sls else (current_price * 1.01)

        # Safety: Final check to ensure no inversion
        if signal == "BUY":
            if sl and sl >= current_price: sl = current_price * 0.995
            if tp and tp <= current_price: tp = current_price * 1.01
        elif signal == "SELL":
            if sl and sl <= current_price: sl = current_price * 1.005
            if tp and tp >= current_price: tp = current_price * 0.99

        # Generate Reasoning String
        reasons = []
        if structure_info['last_bos'] == ("BULLISH" if structure_info['trend_direction'] == 1 else "BEARISH"):
            reasons.append("Structure Alignment (+20)")
        if liquidity_info['sweep_detected']:
            reasons.append(f"Liquidity Sweep {liquidity_info['sweep_detected']} (+15)")
        if displacement_info['displacement_score'] > 0:
            reasons.append(f"Displacement Momentum (+{displacement_info['displacement_score']})")
        if regime == 'TRENDING_STRONG':
            reasons.append("Strong Trend Alignment (+15)")
        
        reasoning = " | ".join(reasons) if reasons else "Confluence score accumulation"

        return {
            'signal': signal,
            'strength_score': score,
            'score': score, # Alias for convenience
            'threshold': threshold,
            'reasoning': reasoning,
            'structural_sl': sl,
            'structural_tp': tp,
            'regime_penalty_boost': REGIMES.get(regime, {}).get('boost', 0)
        }
