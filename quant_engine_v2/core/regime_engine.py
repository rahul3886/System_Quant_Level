import numpy as np
import pandas as pd
from quant_engine_v2.configs.regime_config import *

class RegimeEngine:
    def __init__(self):
        pass

    def calculate_regime(self, df, structure_info):
        # 1. Trend Persistence
        # Using simple HH/LL counters from structure_info or raw price if needed
        # For now, let's use a windows approach on OHLC
        
        returns = df['close'].pct_change()
        volatility = returns.std() * np.sqrt(252) # annualized vol
        
        # 2. Volatility Percentile
        # ATR / ATR percentile
        df['atr'] = self._calculate_atr(df)
        current_atr = df['atr'].iloc[-1]
        atr_percentile = df['atr'].rolling(window=100).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])
        current_perc = atr_percentile.iloc[-1] * 100 if not np.isnan(atr_percentile.iloc[-1]) else 50
        
        vol_state = "NORMAL_VOL"
        if current_perc >= VOLATILITY_PERCENTILE_HIGH:
            vol_state = "HIGH_VOL"
        elif current_perc <= VOLATILITY_PERCENTILE_LOW:
            vol_state = "LOW_VOL"

        # 3. Compression Ratio
        # range_last_20 / ATR_last_20
        last_range = df['high'].rolling(20).max() - df['low'].rolling(20).min()
        avg_atr = df['atr'].rolling(20).mean()
        compression_ratio = (last_range / avg_atr).iloc[-1]
        
        # 4. Displacement Frequency
        # count bodies > 1.2 * ATR
        df['body_size'] = (df['close'] - df['open']).abs()
        df['is_displacement'] = df['body_size'] > (1.2 * df['atr'])
        displacement_count = df['is_displacement'].tail(DISPLACEMENT_FREQ_LOOKBACK).sum()
        
        # 5. Regime Assignment
        regime = "RANGING"
        confidence_score = 50
        
        if displacement_count >= DISPLACEMENT_FREQ_THRESHOLD:
            regime = "EXPANSION"
            confidence_score = 70
        
        if compression_ratio < COMPRESSION_RATIO_THRESHOLD:
            regime = "COMPRESSION"
            confidence_score = 80
            
        if structure_info['trend_direction'] != 0:
            if vol_state == "HIGH_VOL" and displacement_count >= 2:
                regime = "TRENDING_STRONG"
                confidence_score = 90
            else:
                regime = "TRENDING_WEAK"
                confidence_score = 60
        
        # If Alternating BOS -> RANGING (simplified here)
        if structure_info['last_bos'] is None:
             regime = "RANGING"

        return {
            'regime': regime,
            'volatility_state': vol_state,
            'confidence_score': confidence_score,
            'compression_ratio': compression_ratio,
            'displacement_count': displacement_count
        }

    def _calculate_atr(self, df, period=14):
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift()).abs()
        low_close = (df['low'] - df['close'].shift()).abs()
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(window=period).mean()
