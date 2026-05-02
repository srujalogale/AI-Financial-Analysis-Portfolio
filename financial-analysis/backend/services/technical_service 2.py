import numpy as np
import pandas as pd


def compute_all_indicators(df: pd.DataFrame) -> dict:
    result = {}
    for ticker in df.columns:
        prices = df[ticker].dropna()
        result[ticker] = {
            "rsi": _rsi(prices),
            "macd": _macd(prices),
            "bollinger": _bollinger(prices),
            "moving_averages": _moving_averages(prices),
            "signal": _trade_signal(prices),
        }
    return result


def _rsi(prices: pd.Series, period: int = 14) -> dict:
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    val = round(float(rsi.iloc[-1]), 2) if not rsi.empty else 50.0
    signal = "Overbought" if val > 70 else "Oversold" if val < 30 else "Neutral"
    return {"value": val, "signal": signal, "series": rsi.dropna().tail(30).round(2).tolist()}


def _macd(prices: pd.Series) -> dict:
    ema12 = prices.ewm(span=12, adjust=False).mean()
    ema26 = prices.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    macd_val = round(float(macd_line.iloc[-1]), 4)
    sig_val = round(float(signal_line.iloc[-1]), 4)
    hist_val = round(float(histogram.iloc[-1]), 4)
    trend = "Bullish" if macd_val > sig_val else "Bearish"
    return {
        "macd": macd_val,
        "signal": sig_val,
        "histogram": hist_val,
        "trend": trend,
        "macd_series": macd_line.tail(30).round(4).tolist(),
        "signal_series": signal_line.tail(30).round(4).tolist(),
    }


def _bollinger(prices: pd.Series, period: int = 20, std: int = 2) -> dict:
    sma = prices.rolling(period).mean()
    stddev = prices.rolling(period).std()
    upper = sma + std * stddev
    lower = sma - std * stddev
    price = float(prices.iloc[-1])
    u = float(upper.iloc[-1])
    l = float(lower.iloc[-1])
    m = float(sma.iloc[-1])
    pct_b = round((price - l) / (u - l) * 100, 2) if (u - l) > 0 else 50.0
    position = "Above Upper" if price > u else "Below Lower" if price < l else "Within Bands"
    return {
        "upper": round(u, 2), "middle": round(m, 2), "lower": round(l, 2),
        "pct_b": pct_b, "bandwidth": round((u - l) / m * 100, 2),
        "position": position,
        "upper_series": upper.tail(30).round(2).tolist(),
        "lower_series": lower.tail(30).round(2).tolist(),
        "sma_series": sma.tail(30).round(2).tolist(),
    }


def _moving_averages(prices: pd.Series) -> dict:
    price = float(prices.iloc[-1])
    mas = {}
    for w in [20, 50, 200]:
        if len(prices) >= w:
            val = round(float(prices.rolling(w).mean().iloc[-1]), 2)
            mas[f"ma{w}"] = {"value": val, "above": price > val}
    return mas


def _trade_signal(prices: pd.Series) -> dict:
    rsi_val = _rsi(prices)["value"]
    macd_d = _macd(prices)
    bb = _bollinger(prices)
    score = 0
    reasons = []
    if rsi_val < 35:
        score += 1; reasons.append("RSI oversold")
    elif rsi_val > 65:
        score -= 1; reasons.append("RSI overbought")
    if macd_d["macd"] > macd_d["signal"]:
        score += 1; reasons.append("MACD bullish crossover")
    else:
        score -= 1; reasons.append("MACD bearish crossover")
    if bb["position"] == "Below Lower":
        score += 1; reasons.append("Below Bollinger lower band")
    elif bb["position"] == "Above Upper":
        score -= 1; reasons.append("Above Bollinger upper band")

    if score >= 2: action = "STRONG BUY"
    elif score == 1: action = "BUY"
    elif score == -1: action = "SELL"
    elif score <= -2: action = "STRONG SELL"
    else: action = "HOLD"
    return {"action": action, "score": score, "reasons": reasons}
