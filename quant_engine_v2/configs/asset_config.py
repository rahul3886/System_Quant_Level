# quant_engine_v2/configs/asset_config.py

ASSETS = {
    'CRYPTO': {
        'symbols': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOGE/USDT', 'BNB/USDT', 'LTC/USDT'],
        'exchange': 'binance',
        'provider': 'ccxt'
    },
    'FOREX': {
        'symbols': ['EURUSD', 'EURAUD', 'GBPUSD', 'GBPJPY', 'USDJPY', 'EURJPY', 'USDCHF'],
        'provider': 'mt5',
        'fallback': 'yfinance'
    },
    'METALS': {
        'symbols': ['XAUUSD', 'XAGUSD', 'XAUEUR'],
        'provider': 'mt5',
        'fallback': 'yfinance'
    }
}

TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h', '1d']

# Mapping for MT5 symbols if they differ from standard
MT5_SYMBOL_MAP = {
    'XAUUSD': 'XAUUSD',
    'EURUSD': 'EURUSD',
    # Add mapping if needed for specific brokers
}
