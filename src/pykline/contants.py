MAIN_PANE_ID = "candle_pane"

# Default Indicators
# key: indicator name
# {
#     "params": default params list,
#     "params_n": -1,  # -1: variable number of parameters; >=0: fixed number of parameters
#     "overlay": True # whether the indicator is an overlay on the main pane
# }
DEFAULT_INDICATORS = {
    "MA": {"params": [5, 10, 30, 60], "params_n": -1, "overlay": True},
    "EMA": {"params": [6, 12, 20], "params_n": -1, "overlay": True},
    "SMA": {"params": [12, 2], "params_n": 2, "overlay": True},
    "BBI": {"params": [3, 6, 12, 24], "params_n": 4, "overlay": True},
    "VOL": {"params": [5, 10, 20], "params_n": -1, "overlay": False},
    "MACD": {"params": [12, 26, 9], "params_n": 3, "overlay": False},
    "BOLL": {"params": [20, 2], "params_n": 2, "overlay": True},
    "KDJ": {"params": [9, 3, 3], "params_n": 3, "overlay": False},
    "RSI": {"params": [6, 12, 24], "params_n": 3, "overlay": False},
    "BIAS": {"params": [6, 12, 24], "params_n": 3, "overlay": False},
    "BRAR": {"params": [26], "params_n": 1, "overlay": False},
    "CCI": {"params": [13], "params_n": 1, "overlay": False},
    "DMI": {"params": [14, 6], "params_n": 2, "overlay": False},
    "CR": {"params": [26, 10, 20, 40, 60], "params_n": 5, "overlay": False},
    "PSY": {"params": [12, 6], "params_n": 2, "overlay": False},
    "DMA": {"params": [10, 50, 10], "params_n": 3, "overlay": False},
    "TRIX": {"params": [12, 20], "params_n": 2, "overlay": False},
    "OBV": {"params": [30], "params_n": 1, "overlay": False},
    "VR": {"params": [24, 30], "params_n": 2, "overlay": False},
    "WR": {
        "params": [6, 10, 14],
        "params_n": -1,
        "overlay": False,
    },
    "MTM": {"params": [6, 10], "params_n": 2, "overlay": False},
    "EMV": {"params": [14, 9], "params_n": 2, "overlay": False},
    "ROC": {"params": [12, 6], "params_n": 2, "overlay": False},
    "SAR": {"params": [2, 2, 20], "params_n": 3, "overlay": True},
    "AO": {"params": [5, 34], "params_n": 2, "overlay": False},
    "PVT": {
        "params": [],
        "params_n": 0,
        "overlay": False,
    },
    "AVP": {
        "params": [],
        "params_n": 0,
        "overlay": False,
    },
}
