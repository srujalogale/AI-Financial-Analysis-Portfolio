import yfinance as yf
import pandas as pd
from utils.helpers import validate_tickers


def fetch_market_data(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    validate_tickers(tickers)
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)

    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            df = raw["Close"]
        elif "Price" in raw.columns.get_level_values(0):
            df = raw["Price"]
        else:
            df = raw.xs(raw.columns.get_level_values(0)[0], axis=1, level=0)
    elif "Close" in raw.columns:
        df = raw[["Close"]]
        df.columns = [tickers[0]] if len(tickers) == 1 else tickers
    else:
        df = raw
        if df.shape[1] == len(tickers):
            df.columns = tickers

    df = df.ffill().dropna(how="all")

    if df.empty:
        raise ValueError("No data returned for given tickers/period.")

    # Drop tickers with too many missing values (>20%)
    threshold = len(df) * 0.8
    df = df.dropna(axis=1, thresh=int(threshold))

    return df
