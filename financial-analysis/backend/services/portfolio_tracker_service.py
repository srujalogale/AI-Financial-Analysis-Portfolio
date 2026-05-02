import numpy as np
import pandas as pd
from services.live_data_service import get_live_quote


def analyze_portfolio(holdings: list[dict]) -> dict:
    """
    holdings: [{"ticker": "AAPL", "shares": 10, "avg_cost": 150.0}, ...]
    """
    enriched = []
    total_invested = 0
    total_current = 0

    for h in holdings:
        ticker = h["ticker"]
        shares = float(h["shares"])
        avg_cost = float(h["avg_cost"])

        try:
            quote = get_live_quote(ticker)
            current_price = quote["price"]
        except Exception:
            current_price = avg_cost

        invested = shares * avg_cost
        current_val = shares * current_price
        pnl = current_val - invested
        pnl_pct = (pnl / invested * 100) if invested > 0 else 0

        total_invested += invested
        total_current += current_val

        enriched.append({
            "ticker": ticker,
            "shares": shares,
            "avg_cost": round(avg_cost, 2),
            "current_price": round(current_price, 2),
            "invested": round(invested, 2),
            "current_value": round(current_val, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 2),
            "name": quote.get("name", ticker) if isinstance(quote, dict) else ticker,
            "day_change_pct": quote.get("change_pct", 0) if isinstance(quote, dict) else 0,
        })

    total_pnl = total_current - total_invested
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0

    # Allocation %
    for e in enriched:
        e["allocation_pct"] = round(e["current_value"] / total_current * 100, 2) if total_current > 0 else 0

    # Sort by allocation
    enriched.sort(key=lambda x: -x["current_value"])

    return {
        "holdings": enriched,
        "summary": {
            "total_invested": round(total_invested, 2),
            "total_current_value": round(total_current, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round(total_pnl_pct, 2),
            "best_performer": max(enriched, key=lambda x: x["pnl_pct"])["ticker"] if enriched else None,
            "worst_performer": min(enriched, key=lambda x: x["pnl_pct"])["ticker"] if enriched else None,
            "num_holdings": len(enriched),
        }
    }


def compare_stocks(tickers: list[str], period: str = "1y") -> dict:
    import yfinance as yf
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        df = raw["Close"]
    else:
        df = raw
    df = df.ffill().dropna()
    norm = (df / df.iloc[0] * 100).round(2)
    returns = df.pct_change().dropna()

    stats = {}
    for t in df.columns:
        r = returns[t].dropna()
        stats[t] = {
            "total_return_pct": round((df[t].iloc[-1] / df[t].iloc[0] - 1) * 100, 2),
            "volatility": round(float(r.std() * np.sqrt(252) * 100), 2),
            "sharpe": round(float((r.mean() * 252 - 0.05) / (r.std() * np.sqrt(252))), 3) if r.std() > 0 else 0,
            "max_drawdown": round(float(((1 + r).cumprod() / (1 + r).cumprod().cummax() - 1).min() * 100), 2),
        }

    return {
        "tickers": list(df.columns),
        "normalized": {t: norm[t].tolist() for t in df.columns},
        "dates": [str(d.date()) for d in df.index],
        "stats": stats,
        "correlation": returns.corr().round(3).to_dict(),
    }
