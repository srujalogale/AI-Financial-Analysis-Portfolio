import yfinance as yf
import pandas as pd
import numpy as np

DEFAULT_UNIVERSE = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
    "JPM", "JNJ", "V", "UNH", "XOM", "PG", "MA", "HD", "CVX", "MRK",
    "ABBV", "PEP", "KO", "AVGO", "COST", "TMO", "MCD", "ACN", "LIN",
    "DHR", "NEE", "WMT", "AMD", "INTC", "QCOM", "TXN", "IBM"
]


def screen_stocks(
    min_return: float = 0.0,
    max_volatility: float = 0.5,
    min_sharpe: float = 0.5,
    universe: list[str] = None,
    period: str = "1y",
    top_n: int = 10,
) -> dict:
    tickers = universe or DEFAULT_UNIVERSE
    try:
        raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
        if isinstance(raw.columns, pd.MultiIndex):
            df = raw["Close"]
        else:
            df = raw
        df = df.ffill().dropna(how="all")
    except Exception as e:
        return {"error": str(e), "results": []}

    returns = df.pct_change().dropna()
    results = []

    for t in df.columns:
        try:
            r = returns[t].dropna()
            if len(r) < 20: continue
            ann_return = float(r.mean() * 252)
            vol = float(r.std() * np.sqrt(252))
            sharpe = (ann_return - 0.05) / vol if vol > 0 else 0
            max_dd = float(((1 + r).cumprod() / (1 + r).cumprod().cummax() - 1).min())

            if ann_return >= min_return and vol <= max_volatility and sharpe >= min_sharpe:
                results.append({
                    "ticker": t,
                    "annual_return_pct": round(ann_return * 100, 2),
                    "volatility_pct": round(vol * 100, 2),
                    "sharpe_ratio": round(sharpe, 3),
                    "max_drawdown_pct": round(max_dd * 100, 2),
                    "score": round(sharpe * 0.5 + ann_return * 0.3 - vol * 0.2, 4),
                })
        except Exception:
            continue

    results.sort(key=lambda x: -x["score"])
    return {
        "filters": {"min_return": min_return, "max_volatility": max_volatility, "min_sharpe": min_sharpe},
        "total_screened": len(tickers),
        "passed": len(results),
        "results": results[:top_n],
    }
