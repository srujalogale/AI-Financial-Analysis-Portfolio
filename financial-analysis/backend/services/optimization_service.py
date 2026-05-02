import numpy as np
import pandas as pd
from scipy.optimize import minimize
from services.risk_service import RISK_FREE_RATE, TRADING_DAYS

RISK_TARGETS = {
    "low": {"target": "min_vol", "constraints": {"max_weight": 0.25}},
    "medium": {"target": "max_sharpe", "constraints": {"max_weight": 0.35}},
    "high": {"target": "max_return", "constraints": {"max_weight": 0.50}},
}


def optimize_portfolio(returns: pd.DataFrame, risk_level: str = "medium") -> tuple[np.ndarray, dict]:
    tickers = returns.columns.tolist()
    n = len(tickers)
    mu = returns.mean().values * TRADING_DAYS
    cov = returns.cov().values * TRADING_DAYS
    config = RISK_TARGETS[risk_level]
    max_w = config["constraints"]["max_weight"]

    bounds = [(0.01, max_w)] * n
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

    target = config["target"]
    if target == "max_sharpe":
        obj = lambda w: -_sharpe(w, mu, cov)
    elif target == "min_vol":
        obj = lambda w: _volatility(w, cov)
    else:
        obj = lambda w: -_expected_return(w, mu)

    x0 = np.ones(n) / n
    result = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                      options={"maxiter": 1000, "ftol": 1e-9})

    weights = result.x if result.success else x0
    weights = np.clip(weights, 0, 1)
    weights /= weights.sum()

    port_series = pd.Series(returns.values @ weights)
    cum = (1 + port_series).cumprod()
    max_dd = float(((cum / cum.cummax()) - 1).min())
    var_95 = float(np.percentile(port_series.dropna(), 5))

    stats = {
        "expected_return": round(float(_expected_return(weights, mu)), 4),
        "volatility": round(float(_volatility(weights, cov)), 4),
        "sharpe_ratio": round(float(_sharpe(weights, mu, cov)), 4),
        "max_drawdown": round(max_dd, 4),
        "var_95": round(var_95, 4),
        "weights": {t: round(float(w), 4) for t, w in zip(tickers, weights)},
    }
    return weights, stats


def efficient_frontier(returns: pd.DataFrame, n_points: int = 30) -> list[dict]:
    tickers = returns.columns.tolist()
    n = len(tickers)
    mu = returns.mean().values * TRADING_DAYS
    cov = returns.cov().values * TRADING_DAYS
    min_ret, max_ret = mu.min(), mu.max()
    frontier = []
    for target_ret in np.linspace(min_ret, max_ret, n_points):
        constraints = [
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},
            {"type": "eq", "fun": lambda w, r=target_ret: _expected_return(w, mu) - r},
        ]
        result = minimize(lambda w: _volatility(w, cov), np.ones(n) / n,
                          method="SLSQP", bounds=[(0.0, 1.0)] * n, constraints=constraints)
        if result.success:
            frontier.append({"return": round(float(target_ret), 4),
                             "volatility": round(float(_volatility(result.x, cov)), 4)})
    return frontier


def _expected_return(w, mu): return float(w @ mu)
def _volatility(w, cov): return float(np.sqrt(w @ cov @ w))
def _sharpe(w, mu, cov):
    vol = _volatility(w, cov)
    return (_expected_return(w, mu) - RISK_FREE_RATE * TRADING_DAYS) / vol if vol > 0 else 0.0
