import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_percentage_error


def predict_prices(df: pd.DataFrame, ticker: str, days_ahead: int = 7) -> dict:
    prices = df[ticker].dropna()
    if len(prices) < 60:
        return {"error": "Insufficient data for prediction (need 60+ days)"}

    lr_result = _linear_regression(prices, days_ahead)
    rf_result = _random_forest(prices, days_ahead)

    current = float(prices.iloc[-1])
    avg_pred = (lr_result["predictions"][-1] + rf_result["predictions"][-1]) / 2
    direction = "UP" if avg_pred > current else "DOWN"
    confidence = min(abs(avg_pred - current) / current * 100 * 10, 95)

    return {
        "ticker": ticker,
        "current_price": round(current, 2),
        "days_ahead": days_ahead,
        "linear_regression": lr_result,
        "random_forest": rf_result,
        "ensemble": {
            "predictions": [round((lr_result["predictions"][i] + rf_result["predictions"][i]) / 2, 2)
                           for i in range(days_ahead)],
            "direction": direction,
            "confidence_pct": round(confidence, 1),
            "signal": _buy_sell_signal(current, avg_pred),
        },
        "historical_tail": prices.tail(30).round(2).tolist(),
    }


def _make_features(prices: pd.Series, lookback: int = 10):
    X, y = [], []
    vals = prices.values
    for i in range(lookback, len(vals)):
        X.append(vals[i - lookback:i])
        y.append(vals[i])
    return np.array(X), np.array(y)


def _linear_regression(prices: pd.Series, days_ahead: int) -> dict:
    lookback = 10
    X, y = _make_features(prices, lookback)
    split = int(len(X) * 0.8)
    model = LinearRegression()
    model.fit(X[:split], y[:split])
    mape = mean_absolute_percentage_error(y[split:], model.predict(X[split:])) * 100

    window = prices.values[-lookback:].tolist()
    preds = []
    for _ in range(days_ahead):
        p = float(model.predict([window[-lookback:]])[0])
        preds.append(round(p, 2))
        window.append(p)

    return {"predictions": preds, "mape": round(mape, 2), "model": "Linear Regression"}


def _random_forest(prices: pd.Series, days_ahead: int) -> dict:
    lookback = 20
    X, y = _make_features(prices, lookback)
    split = int(len(X) * 0.8)
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X[:split], y[:split])
    mape = mean_absolute_percentage_error(y[split:], model.predict(X[split:])) * 100

    window = prices.values[-lookback:].tolist()
    preds = []
    for _ in range(days_ahead):
        p = float(model.predict([window[-lookback:]])[0])
        preds.append(round(p, 2))
        window.append(p)

    return {"predictions": preds, "mape": round(mape, 2), "model": "Random Forest"}


def _buy_sell_signal(current: float, predicted: float) -> str:
    change_pct = (predicted - current) / current * 100
    if change_pct > 3: return "STRONG BUY"
    if change_pct > 1: return "BUY"
    if change_pct < -3: return "STRONG SELL"
    if change_pct < -1: return "SELL"
    return "HOLD"
