import json
from typing import List, Dict

MAIN_PANE_ID = "candle_pane"

# Default Indicators
# key: indicator name
# {
#     "params": default params list,
#     "params_n": -1,  # -1: variable number of parameters; >=0: fixed number of parameters
#     "overlay": True # whether the indicator is an overlay on the main pane
# }
DEFAULT_INDICATORS = {
    "MA": {
        "params": [5, 10, 30, 60],
        "params_n": -1,
        "overlay": True,
        "name_en": "Moving Average",
        "name_cn": "移动平均线"
    },
    "EMA": {
        "params": [6, 12, 20],
        "params_n": -1,
        "overlay": True,
        "name_en": "Exponential Moving Average",
        "name_cn": "指数平滑移动平均线"
    },
    "SMA": {
        "params": [12, 2],
        "params_n": 2,
        "overlay": True,
        "name_en": "Simple Moving Average",
        "name_cn": "简单移动平均线"
    },
    "BBI": {
        "params": [3, 6, 12, 24],
        "params_n": 4,
        "overlay": True,
        "name_en": "Bull and Bear Index",
        "name_cn": "多空指标"
    },
    "VOL": {
        "params": [5, 10, 20],
        "params_n": -1,
        "overlay": False,
        "name_en": "Volume",
        "name_cn": "成交量"
    },
    "MACD": {
        "params": [12, 26, 9],
        "params_n": 3,
        "overlay": False,
        "name_en": "Moving Average Convergence Divergence",
        "name_cn": "指数平滑异同平均线"
    },
    "BOLL": {
        "params": [20, 2],
        "params_n": 2,
        "overlay": True,
        "name_en": "Bollinger Bands",
        "name_cn": "布林线"
    },
    "KDJ": {
        "params": [9, 3, 3],
        "params_n": 3,
        "overlay": False,
        "name_en": "Stochastic Oscillator",
        "name_cn": "随机指标"
    },
    "RSI": {
        "params": [6, 12, 24],
        "params_n": 3,
        "overlay": False,
        "name_en": "Relative Strength Index",
        "name_cn": "相对强弱指数"
    },
    "BIAS": {
        "params": [6, 12, 24],
        "params_n": 3,
        "overlay": False,
        "name_en": "Bias Ratio",
        "name_cn": "乖离率"
    },
    "BRAR": {
        "params": [26],
        "params_n": 1,
        "overlay": False,
        "name_en": "BRAR Indicator",
        "name_cn": "情绪指标"
    },
    "CCI": {
        "params": [13],
        "params_n": 1,
        "overlay": False,
        "name_en": "Commodity Channel Index",
        "name_cn": "顺势指标"
    },
    "DMI": {
        "params": [14, 6],
        "params_n": 2,
        "overlay": False,
        "name_en": "Directional Movement Index",
        "name_cn": "趋向指标"
    },
    "CR": {
        "params": [26, 10, 20, 40, 60],
        "params_n": 5,
        "overlay": False,
        "name_en": "CR Indicator",
        "name_cn": "能量指标"
    },
    "PSY": {
        "params": [12, 6],
        "params_n": 2,
        "overlay": False,
        "name_en": "Psychological Line",
        "name_cn": "心理线"
    },
    "DMA": {
        "params": [10, 50, 10],
        "params_n": 3,
        "overlay": False,
        "name_en": "Different of Moving Average",
        "name_cn": "平行线差指标"
    },
    "TRIX": {
        "params": [12, 20],
        "params_n": 2,
        "overlay": False,
        "name_en": "Triple Exponential Average",
        "name_cn": "三重指数平滑平均线"
    },
    "OBV": {
        "params": [30],
        "params_n": 1,
        "overlay": False,
        "name_en": "On Balance Volume",
        "name_cn": "能量潮"
    },
    "VR": {
        "params": [24, 30],
        "params_n": 2,
        "overlay": False,
        "name_en": "Volume Ratio",
        "name_cn": "成交量比率"
    },
    "WR": {
        "params": [6, 10, 14],
        "params_n": -1,
        "overlay": False,
        "name_en": "Williams %R",
        "name_cn": "威廉指标"
    },
    "MTM": {
        "params": [6, 10],
        "params_n": 2,
        "overlay": False,
        "name_en": "Momentum Indicator",
        "name_cn": "动量指标"
    },
    "EMV": {
        "params": [14, 9],
        "params_n": 2,
        "overlay": False,
        "name_en": "Ease of Movement",
        "name_cn": "简易波动指标"
    },
    "ROC": {
        "params": [12, 6],
        "params_n": 2,
        "overlay": False,
        "name_en": "Rate of Change",
        "name_cn": "变动率指标"
    },
    "SAR": {
        "params": [2, 2, 20],
        "params_n": 3,
        "overlay": True,
        "name_en": "Stop and Reverse",
        "name_cn": "抛物线指标"
    },
    "AO": {
        "params": [5, 34],
        "params_n": 2,
        "overlay": False,
        "name_en": "Awesome Oscillator",
        "name_cn": "动量震荡指标"
    },
    "PVT": {
        "params": [],
        "params_n": 0,
        "overlay": False,
        "name_en": "Price Volume Trend",
        "name_cn": "价量趋势指标"
    },
    "AVP": {
        "params": [],
        "params_n": 0,
        "overlay": False,
        "name_en": "Average Price",
        "name_cn": "平均价格线"
    },
}


def list_indicators(lang="en", do_print=False) -> List[Dict]:
    if lang == "en":
        supports = [{"name": k, "default": v['params'], "description": v['name_en']}
                    for k, v in DEFAULT_INDICATORS.items()]
    else:
        supports = [{"name": k, "default": v['params'], "description": v['name_cn']}
                    for k, v in DEFAULT_INDICATORS.items()]
    if do_print:
        # Calculate column widths
        name_width = max(len(ind['name']) for ind in supports) + 4
        param_width = max(len(', '.join(map(str, ind['default']))) for ind in supports) + 4
        desc_width = max(len(ind['description']) for ind in supports) + 4

        # Build header
        header = (f"{'name':<{name_width}} {'default':<{param_width}} {'description':<{desc_width}}")
        separator = "-" * (name_width + param_width + desc_width + 4)

        print(header)
        print(separator)

        # Print each indicator
        for ind in supports:
            params = ', '.join(map(str, ind['default'])) if ind['default'] else 'None'
            print(f"{ind['name']:<{name_width}} {params:<{param_width}} {ind['description']:<{desc_width}}")

        print(f"\nTotal indicators: {len(supports)}")
    return supports
