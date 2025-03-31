import pandas as pd
from .indicator import Indicator
from .render import render_html
from typing import List, Dict, Union, Tuple, TypedDict


class Fields(TypedDict, total=False):
    timestamp: str
    open: str
    close: str
    high: str
    low: str
    volume: str
    turnover: str


FIELDS_REQUIRED = ["timestamp", "open", "close", "high", "low"]


class Chart:

    def _check_required_fields(self) -> None:
        """
        Check if required fields are present in renamed DataFrame
        Raises:
            ValueError if any required field is missing
        """
        columns = self.kline.columns
        for field in FIELDS_REQUIRED:
            if field not in columns:
                raise ValueError(f"Required field `{field}` not found in DataFrame!")

    def _convert_timestamp(self) -> None:
        """
        Convert timestamp column to integer milliseconds (ms)

        Handles:
        - Numeric timestamps (seconds, milliseconds, microseconds)
        - String timestamps (ISO format, etc.)
        - Ensures final output is always milliseconds as int64
        """
        if "timestamp" not in self.kline.columns:
            raise ValueError("timestamp column not found in DataFrame")

        ts_series = self.kline["timestamp"]

        # Attempt numeric conversion first
        ts_numeric = pd.to_numeric(ts_series, errors="coerce")
        if ts_numeric.notna().all():
            # Handle numeric timestamps
            max_ts = ts_numeric.max()
            if max_ts < 1e10:  # Unix seconds
                ts_millis = ts_numeric * 1000
            elif max_ts < 1e13:  # Already milliseconds
                ts_millis = ts_numeric
            elif max_ts < 1e16:  # Microseconds
                ts_millis = ts_numeric // 1000  # Convert to milliseconds
            else:  # nanoseconds
                ts_millis = ts_numeric // 10 ** 6  # Convert to nanoseconds
            datetime_series = ts_millis.astype("int64")
        else:
            # Parse string timestamps
            datetime_series = (
                    pd.to_datetime(ts_series).view("int64") // 10 ** 6
            ).astype("int64")

        # Set timestamp column
        self.kline.loc[:, "timestamp"] = datetime_series

    def data(self,
             df: pd.DataFrame,
             fields: Fields = None, ) -> "Chart":
        """
        Add data to chart

        Args:
            df: pandas DataFrame:
                The DataFrame which contains kline data
                Example df:
                         timestamp     open     high      low    close  volume
                0    1517846400000   7424.6   7511.3   6032.3   7310.1  224461
                1    1517932800000   7310.1   8499.9   6810.0   8165.4  148807
                2    1518019200000   8166.7   8700.8   7400.0   8245.1   24467
                3    1518105600000   8244.0   8494.0   7760.0   8364.0   29834
                4    1518192000000   8363.6   9036.7   8269.8   8311.9   28203

            fields: dict of renamed fields
                The key is target field name, and the value is original column name.
                Required fields are "timestamp", "open", "close", "high", "low".
                Optional fields are "volume", "turnover".

                If your dataframe's column names are not named as above,
                you can use the fields parameter to rename them:
                Example df which need fields parameter:
                                dt        o        h        l        c  volume
                0    1517846400000   7424.6   7511.3   6032.3   7310.1  224461
                1    1517932800000   7310.1   8499.9   6810.0   8165.4  148807
                2    1518019200000   8166.7   8700.8   7400.0   8245.1   24467
                3    1518105600000   8244.0   8494.0   7760.0   8364.0   29834
                4    1518192000000   8363.6   9036.7   8269.8   8311.9   28203
                The fields parameter should be:
                fields = {
                    "timestamp": "dt",
                    "open": "o",
                    "close": "c",
                    "high": "h",
                    "low": "l",
                }
        """
        if len(df) == 0 or df.empty:
            raise ValueError("DataFrame is empty!")

        self.kline: pd.DataFrame = df.copy()
        if fields is not None:
            self.kline = self.kline.rename(columns={v: k for k, v in fields.items()})
        self._check_required_fields()
        self._convert_timestamp()
        self._indicators: List[Indicator] = []

        return self

    def indicator(
            self,
            indicator: Union[str, List[Union[str, List, Tuple, Dict]]],
            params: List[int] = None,
            overlay: bool = False,
    ) -> "Chart":
        """
        Add technical indicators to the chart

        Args:
            indicator: Indicator specification, can be:
                - str: Single indicator name (use default params)
                - List[str]: Multiple indicator names
                - List[Tuple]: [(indicator_name, params),(indicator_name, params, overlay) ...]
                - List[Dict]: [{"name": ..., "params": ..., "overlay": ...}, ...]

            params: Default parameters for the indicator
            overlay: Default overlay setting for the indicator

        Raises:
            ValueError: If indicator name is invalid or parameters don't match requirements

        Example::
            # Add single indicator with default params
            chart.indicator("MA")

            # Add multiple indicators
            chart.indicator(["MACD", "RSI"])

            # Custom parameters
            chart.indicator([("MA", [5, 10], True), ("RSI", [14])])

            # Full specification
            chart.indicator([
                {"name": "BOLL", "params": [20, 2], "overlay": True},
                {"name": "VOL", "params": [5, 10]}
            ])
        """
        if isinstance(indicator, str):
            self._indicators.append(Indicator(indicator, params, overlay=overlay))
            return self
        for ind in indicator:
            self._indicators.append(self._parse_indicator_spec(ind))
        return self

    def _parse_indicator_spec(
            self, indicator: Union[str, List, Tuple, Dict]
    ) -> Indicator:
        if isinstance(indicator, str):
            return Indicator(indicator)
        elif isinstance(indicator, list) or isinstance(indicator, tuple):
            assert len(indicator) > 0, "Indicator list cannot be empty!"
            if len(indicator) == 1:
                return Indicator(indicator[0])
            elif len(indicator) == 2:
                return Indicator(indicator[0], indicator[1])
            else:
                assert isinstance(
                    indicator[2], bool
                ), "Indicator overlay must be a boolean!"
                return Indicator(indicator[0], indicator[1], overlay=indicator[2])
        elif isinstance(indicator, dict):
            return Indicator(**indicator)
        else:
            raise ValueError("Invalid indicator specification!")

    def show(self, title: str = "Chart", theme: str = "light", **kwargs) -> None:
        context = {
            "title": title,
            "theme": theme,
            "data": self.kline.to_dict(orient="records"),
            "indicators": [ind.to_html() for ind in self._indicators],
            "resized": kwargs.get("resized", True),
            "width": kwargs.get("width", "100%"),
            "height": kwargs.get("height", "98vh"),
        }

        render_html(context)
