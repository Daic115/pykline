import pykline
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('./example.csv')
    (
        pykline.chart()
        .data(df)
        .indicator([("EMA", [5, 15, 30]), "VOL", "MACD"])
        .show()
    )
