import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_live_quote(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    info = t.info
    hist = t.history(period="2d", interval="1d")

    price = info.get("currentPrice") or info.get("regularMarketPrice") or (float(hist["Close"].iloc[-1]) if not hist.empty else 0)
    prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose") or (float(hist["Close"].iloc[-2]) if len(hist) >= 2 else price)
    change = price - prev_close
    change_pct = (change / prev_close * 100) if prev_close else 0

    return {
        "ticker": ticker,
        "price": round(float(price), 2),
        "prev_close": round(float(prev_close), 2),
        "change": round(float(change), 2),
        "change_pct": round(float(change_pct), 2),
        "open": round(float(info.get("open") or info.get("regularMarketOpen") or price), 2),
        "high": round(float(info.get("dayHigh") or info.get("regularMarketDayHigh") or price), 2),
        "low": round(float(info.get("dayLow") or info.get("regularMarketDayLow") or price), 2),
        "volume": int(info.get("volume") or info.get("regularMarketVolume") or 0),
        "avg_volume": int(info.get("averageVolume") or 0),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector", "N/A"),
        "currency": info.get("currency", "USD"),
        "timestamp": datetime.utcnow().isoformat(),
    }


def get_intraday(ticker: str, interval: str = "5m") -> dict:
    t = yf.Ticker(ticker)
    hist = t.history(period="1d", interval=interval)
    if hist.empty:
        hist = t.history(period="5d", interval="1h")
    hist = hist.dropna()
    return {
        "ticker": ticker,
        "interval": interval,
        "timestamps": [str(i) for i in hist.index],
        "open": hist["Open"].round(2).tolist(),
        "high": hist["High"].round(2).tolist(),
        "low": hist["Low"].round(2).tolist(),
        "close": hist["Close"].round(2).tolist(),
        "volume": hist["Volume"].astype(int).tolist(),
    }


def get_multi_quotes(tickers: list[str]) -> list[dict]:
    results = []
    for t in tickers:
        try:
            results.append(get_live_quote(t))
        except Exception as e:
            results.append({"ticker": t, "error": str(e)})
    return results
