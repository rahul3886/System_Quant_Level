# quant_engine_v2/configs/sweet_spots.py

"""
SUCCESSFUL VAULT
This file stores configurations that have been validated as 'High Yielding' 
during historical backtesting sweeps.
"""

SWEET_SPOTS = {
    'BTC/USDT': {
        '5m': {
            'threshold': 80,
            'description': 'High reliability structural setup',
            'baseline_profit_factor': 8.11,
            'baseline_win_rate': 0.71
        }
    },
    'SOL/USDT': {
        '5m': {
            'threshold': 80,
            'description': 'Impulse expansion setup',
            'baseline_profit_factor': 4.82,
            'baseline_win_rate': 0.50
        }
    },
    'BNB/USDT': {
        '1m': {
            'threshold': 60,
            'description': 'High frequency mean reversion',
            'baseline_profit_factor': 3.20,
            'baseline_win_rate': 0.51
        }
    },
    'GBPUSD': {
        '5m': {
            'threshold': 70,
            'description': 'Forex trend persistence',
            'baseline_profit_factor': 2.74,
            'baseline_win_rate': 0.50
        }
    },
    'USDCHF': {
        '1m': {
            'threshold': 80,
            'description': 'Swiss low-vol breakout',
            'baseline_profit_factor': 3.81,
            'baseline_win_rate': 0.40
        }
    },
    'EURAUD': {
        '1m': {
            'threshold': 80,
            'description': 'Cross-pair volatility catch',
            'baseline_profit_factor': 10.39,
            'baseline_win_rate': 0.40
        }
    },
    'XAU/USD': {
        '5m': {
            'threshold': 60,
            'description': 'Trend-following expansion setup',
            'baseline_profit_factor': 3.25,
            'baseline_win_rate': 0.45
        }
    }
}
