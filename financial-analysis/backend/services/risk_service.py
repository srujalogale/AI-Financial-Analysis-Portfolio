import numpy as np
import pandas as pd

RISK_FREE_RATE = 0.05 / 252  # Daily risk-free rate (~5% annual)
TRADING_DAYS = 252


def compute_risk_metrics(returns: pd.Series, benchmark: pd.Series = None) -> dict:
    annual_return = float(returns.mean() * TRADING_DAYS)
    volatility = float(returns.std() * np.sqrt(TRADING_DAYS))
    sharpe = float((returns.mean() - RISK_FREE_RATE) / returns.std() * np.sqrt(TRADING_DAYS)) if returns.std() > 0 else 0.0
    beta = _compute_beta(returns, benchmark) if benchmark is not None else None
    max_dd = _max_drawdown(returns)

    return {
        "annual_return": round(annual_return, 4),
        "volatility": round(volatility, 4),
        "sharpe_ratio": round(sharpe, 4),
        "beta": round(beta, 4) if beta is not None else None,
        "max_drawdown": round(max_dd, 4),
        "var_95": round(float(np.percentile(returns, 5)), 4),
    }


def compute_portfolio_metrics(returns: pd.DataFrame, weights: np.ndarray) -> dict:
    port_returns = returns.values @ weights
    port_series = pd.Series(port_returns)
    return compute_risk_metrics(port_series)


def _compute_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
    aligned = pd.concat([asset_returns, market_returns], axis=1).dropna()
    if len(aligned) < 30:
        return 1.0
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    return float(cov[0, 1] / cov[1, 1]) if cov[1, 1] != 0 else 1.0


def _max_drawdown(returns: pd.Series) -> float:
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    dd = (cum - peak) / peak
    return float(dd.min())
