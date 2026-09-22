import pandas as pd
import numpy as np

class StructureEngine:
    def __init__(self, window=5):
        self.window = window

    def detect_swings(self, df):
        df = df.copy()
        df['swing_high'] = False
        df['swing_low'] = False
        
        for i in range(self.window, len(df) - self.window):
            if all(df['high'].iloc[i] > df['high'].iloc[i-j] for j in range(1, self.window + 1)) and \
               all(df['high'].iloc[i] > df['high'].iloc[i+j] for j in range(1, self.window + 1)):
                df.at[df.index[i], 'swing_high'] = True
            
            if all(df['low'].iloc[i] < df['low'].iloc[i-j] for j in range(1, self.window + 1)) and \
               all(df['low'].iloc[i] < df['low'].iloc[i+j] for j in range(1, self.window + 1)):
                df.at[df.index[i], 'swing_low'] = True
        return df

    def map_structure(self, df):
        df = self.detect_swings(df)
        
        last_high = None
        last_low = None
        structure_state = "RANGING"
        trend_direction = 0 # 1 Bullish, -1 Bearish
        last_bos = None
        last_choch = None
        
        # Simple BOS/CHoCH detection logic
        # If price breaks last swing high -> Bullish BOS
        # If price breaks last swing low -> Bearish BOS
        # CHoCH is when trend flips (e.g., Bearish BOS followed by break of previous lower high)
        
        # For simplicity in this v1, we focus on HH/HL/LH/LL
        peaks = df[df['swing_high']].copy()
        troughs = df[df['swing_low']].copy()
        
        if len(peaks) >= 2:
            if peaks['high'].iloc[-1] > peaks['high'].iloc[-2]:
                structure_state = "HH"
            else:
                structure_state = "LH"
                
        if len(troughs) >= 2:
            if troughs['low'].iloc[-1] > troughs['low'].iloc[-2]:
                structure_state += "_HL"
            else:
                structure_state += "_LL"
        
        # Basic BOS detection
        if len(peaks) > 0 and df['close'].iloc[-1] > peaks['high'].iloc[-1]:
            last_bos = "BULLISH"
            trend_direction = 1
        elif len(troughs) > 0 and df['close'].iloc[-1] < troughs['low'].iloc[-1]:
            last_bos = "BEARISH"
            trend_direction = -1
            
        return {
            'trend_direction': trend_direction,
            'structure_state': structure_state,
            'last_bos': last_bos,
            'last_choch': last_choch,
            'swing_highs': peaks['high'].tolist(),
            'swing_lows': troughs['low'].tolist(),
            'structural_targets': {
                'liquidity_high': peaks['high'].iloc[-1] if len(peaks) > 0 else None,
                'liquidity_low': troughs['low'].iloc[-1] if len(troughs) > 0 else None
            }
        }
    
    def get_structure_data(self, df):
        return self.map_structure(df)
