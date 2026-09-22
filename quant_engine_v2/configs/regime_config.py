# quant_engine_v2/configs/regime_config.py

REGIMES = {
    'TRENDING_STRONG': {
        'threshold': 60,
        'risk_multiplier': 1.0,
        'boost': 15
    },
    'TRENDING_WEAK': {
        'threshold': 65,
        'risk_multiplier': 0.7,
        'boost': 0
    },
    'EXPANSION': {
        'threshold': 70,
        'risk_multiplier': 1.2,
        'boost': 10
    },
    'RANGING': {
        'threshold': 80,
        'risk_multiplier': 0.5,
        'boost': 0
    },
    'COMPRESSION': {
        'threshold': 1000, # Disabled
        'risk_multiplier': 0.0,
        'boost': -30
    }
}

# General parameters
LOOKBACK_PERIOD = 20
VOLATILITY_PERCENTILE_HIGH = 75
VOLATILITY_PERCENTILE_LOW = 25
COMPRESSION_RATIO_THRESHOLD = 1.5
DISPLACEMENT_FREQ_LOOKBACK = 15
DISPLACEMENT_FREQ_THRESHOLD = 3
TREND_PERSISTENCE_THRESHOLD = 3
