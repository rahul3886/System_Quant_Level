import ccxt
import pandas as pd
import numpy as np
import time
from datetime import datetime

class DataProvider:
    def __init__(self):
        self.binance = ccxt.binance()
        self.mt5_initialized = self._init_mt5()

    def get_data(self, symbol, timeframe='1h', limit=100):
        # Auto-route based on symbol naming convention
        if '/' in symbol and 'USD' in symbol:
            return self.get_crypto_data(symbol, timeframe, limit)
        else:
            return self.get_forex_metal_data(symbol, timeframe, limit)

    def _init_mt5(self):
        try:
            import MetaTrader5 as mt5
            if not mt5.initialize():
                return False
            return True
        except ImportError:
            return False

    def get_crypto_data(self, symbol, timeframe='1h', limit=100):
        try:
            ohlcv = self.binance.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            return pd.DataFrame()

    def get_forex_metal_data(self, symbol, timeframe='1h', limit=100):
        if self.mt5_initialized:
            return self._get_mt5_data(symbol, timeframe, limit)
        else:
            return self._get_yfinance_data(symbol, timeframe, limit)

    def _get_mt5_data(self, symbol, timeframe, limit):
        import MetaTrader5 as mt5
        # Map timeframe to MT5 timeframe
        tf_map = {
            '1m': mt5.TIMEFRAME_M1,
            '5m': mt5.TIMEFRAME_M5,
            '15m': mt5.TIMEFRAME_M15,
            '1h': mt5.TIMEFRAME_H1,
            '4h': mt5.TIMEFRAME_H4,
            '1d': mt5.TIMEFRAME_D1
        }
        mt5_tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
        
        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, limit)
        if rates is None or len(rates) == 0:
            print(f"No rates found for {symbol}")
            return self._get_yfinance_data(symbol, timeframe, limit)
        
        df = pd.DataFrame(rates)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'tick_volume']]
        df.rename(columns={'tick_volume': 'volume'}, inplace=True)
        return df

    def _get_yfinance_data(self, symbol, timeframe, limit):
        import yfinance as yf
        # YFinance symbol mapping
        yf_symbol = symbol
        if 'USD' in symbol and len(symbol) == 6:
            yf_symbol = f"{symbol[:3]}{symbol[3:]}=X"
        
        interval_map = {
            '1m': '1m', '5m': '5m', '15m': '15m', '1h': '1h', '1d': '1d'
        }
        interval = interval_map.get(timeframe, '1h')
        
        try:
            df = yf.download(yf_symbol, period='1mo', interval=interval, progress=False)
            df.reset_index(inplace=True)
            df.rename(columns={'Date': 'timestamp', 'Datetime': 'timestamp', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            return df.tail(limit)
        except Exception as e:
            print(f"YFinance error for {yf_symbol}: {e}")
            return pd.DataFrame()
