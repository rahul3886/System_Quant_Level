import pandas as pd
import numpy as np

class DisplacementEngine:
    def __init__(self):
        pass

    def detect_displacement(self, df):
        # ATR-based body expansion
        df = df.copy()
        df['atr'] = self._calculate_atr(df)
        df['body_size'] = (df['close'] - df['open']).abs()
        
        df['is_displacement'] = df['body_size'] > (1.2 * df['atr'])
        
        displacement_detected = df['is_displacement'].iloc[-1]
        displacement_score = 10 if displacement_detected else 0
        
        # Volume spike (current volume > 1.5x average)
        df['avg_volume'] = df['volume'].rolling(20).mean()
        volume_spike = df['volume'].iloc[-1] > (1.5 * df['avg_volume'].iloc[-1])
        if volume_spike:
            displacement_score += 5

        # FVG (Fair Value Gap) / Imbalance Creation
        # Bullish FVG: Low of candle 3 > High of candle 1
        # Bearish FVG: High of candle 3 < Low of candle 1
        imbalance_zones = []
        if len(df) >= 3:
            for i in range(1, len(df)-1):
                # Bullish FVG
                if df['low'].iloc[i+1] > df['high'].iloc[i-1]:
                    imbalance_zones.append({'type': 'BULLISH_FVG', 'top': df['low'].iloc[i+1], 'bottom': df['high'].iloc[i-1]})
                # Bearish FVG
                if df['high'].iloc[i+1] < df['low'].iloc[i-1]:
                    imbalance_zones.append({'type': 'BEARISH_FVG', 'top': df['low'].iloc[i-1], 'bottom': df['high'].iloc[i+1]})

        if any(zone['type'] == ('BULLISH_FVG' if df['close'].iloc[-1] > df['open'].iloc[-1] else 'BEARISH_FVG') for zone in imbalance_zones[-2:]):
             displacement_score += 5

        return {
            'displacement_detected': displacement_detected,
            'displacement_score': displacement_score,
            'imbalance_zones': imbalance_zones[-5:] # Return last 5 zones
        }

    def _calculate_atr(self, df, period=14):
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift()).abs()
        low_close = (df['low'] - df['close'].shift()).abs()
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(window=period).mean()
