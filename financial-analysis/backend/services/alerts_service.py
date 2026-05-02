from services.live_data_service import get_live_quote
from services.technical_service import compute_all_indicators
from services.data_service import fetch_market_data


def check_alerts(ticker: str, price_target: float = None, stop_loss: float = None) -> dict:
    alerts = []
    quote = get_live_quote(ticker)
    price = quote["price"]
    change_pct = quote["change_pct"]

    # Price target
    if price_target and price >= price_target:
        alerts.append({"type": "TARGET_HIT", "severity": "SUCCESS",
                       "message": f"{ticker} reached price target ${price_target}"})

    # Stop loss
    if stop_loss and price <= stop_loss:
        alerts.append({"type": "STOP_LOSS", "severity": "DANGER",
                       "message": f"{ticker} hit stop loss at ${stop_loss}"})

    # Sudden fall
    if change_pct <= -5:
        alerts.append({"type": "SUDDEN_FALL", "severity": "DANGER",
                       "message": f"{ticker} dropped {change_pct:.1f}% today"})
    elif change_pct >= 5:
        alerts.append({"type": "SUDDEN_SURGE", "severity": "SUCCESS",
                       "message": f"{ticker} surged {change_pct:.1f}% today"})

    # Technical signals
    try:
        df = fetch_market_data([ticker], "3mo")
        indicators = compute_all_indicators(df)
        ind = indicators.get(ticker, {})

        rsi_val = ind.get("rsi", {}).get("value", 50)
        if rsi_val > 75:
            alerts.append({"type": "OVERBOUGHT", "severity": "WARNING",
                           "message": f"{ticker} RSI={rsi_val:.0f} — Overbought territory"})
        elif rsi_val < 25:
            alerts.append({"type": "OVERSOLD", "severity": "INFO",
                           "message": f"{ticker} RSI={rsi_val:.0f} — Oversold, potential bounce"})

        macd = ind.get("macd", {})
        if macd.get("trend") == "Bullish" and macd.get("histogram", 0) > 0:
            alerts.append({"type": "MACD_BULLISH", "severity": "INFO",
                           "message": f"{ticker} MACD bullish crossover detected"})

        signal = ind.get("signal", {}).get("action", "HOLD")
        if signal in ("STRONG BUY", "STRONG SELL"):
            alerts.append({"type": "SIGNAL", "severity": "WARNING",
                           "message": f"{ticker} technical signal: {signal}"})
    except Exception:
        pass

    if not alerts:
        alerts.append({"type": "OK", "severity": "SUCCESS",
                       "message": f"{ticker} — No active alerts. Monitoring normal."})

    return {
        "ticker": ticker,
        "current_price": price,
        "day_change_pct": change_pct,
        "alerts": alerts,
        "alert_count": len([a for a in alerts if a["type"] != "OK"]),
    }
