import json
from typing import List
from .contants import DEFAULT_INDICATORS, MAIN_PANE_ID


class Indicator:
    """
    Technical indicator representation

    Attributes:
        name: Indicator name (e.g. "MA", "MACD")
        params: Calculation parameters
        overlay: Whether to overlay on main chart
    """

    name: str
    params: List[int]
    overlay: bool

    def __init__(self, name: str, params: List[int] = None, **kwargs) -> None:
        """
        Initialize technical indicator

        Args:
            name: Indicator name
            params: Calculation parameters (use default if None)
            overlay: Display on main chart
        """
        if name.upper() not in DEFAULT_INDICATORS:
            raise ValueError(
                f"Indicator {name} is not supported! Supported indicators:\n {list(DEFAULT_INDICATORS.keys())}"
            )

        self.name = name.upper()
        indicator = DEFAULT_INDICATORS[self.name]

        if params is None:
            self.params = indicator["params"]
        else:
            if indicator["params_n"] >= 0 and len(params) != indicator["params_n"]:
                raise ValueError(
                    f"Indicator {name} (default: {indicator['params']}) requires {indicator['params_n']} parameters!"
                )
            self.params = [int(p) for p in params]

        self.overlay = kwargs.get("overlay", indicator["overlay"])

        # todo: add more to render
        self.kwargs = kwargs

    def to_config(self) -> List:
        cfg = [{"name": self.name, "calcParams": self.params}]
        if self.overlay:
            cfg.append(self.overlay)
            cfg.append({"id": MAIN_PANE_ID})
        return cfg

    def to_html(self):
        return f"""
        chart.createIndicator({",".join(json.dumps(c) for c in self.to_config())});
        """
