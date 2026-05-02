import numpy as np
from services.risk_service import TRADING_DAYS

RISK_PROFILES = {
    "low": {
        "label": "Conservative",
        "description": "Capital preservation with modest growth. Diversified, lower-volatility assets.",
        "target_return_range": (0.05, 0.12),
        "max_volatility": 0.15,
        "time_factor": 0.8,
    },
    "medium": {
        "label": "Balanced",
        "description": "Growth-oriented with managed risk. Balanced exposure across sectors.",
        "target_return_range": (0.10, 0.20),
        "max_volatility": 0.25,
        "time_factor": 1.0,
    },
    "high": {
        "label": "Aggressive",
        "description": "Maximum growth potential with higher volatility tolerance.",
        "target_return_range": (0.15, 0.40),
        "max_volatility": 0.45,
        "time_factor": 1.2,
    },
}

SENTIMENT_RULES = [
    {"condition": lambda s: s["sharpe_ratio"] > 1.5, "signal": "STRONG BUY", "score": 2},
    {"condition": lambda s: 0.8 < s["sharpe_ratio"] <= 1.5, "signal": "BUY", "score": 1},
    {"condition": lambda s: 0.3 < s["sharpe_ratio"] <= 0.8, "signal": "HOLD", "score": 0},
    {"condition": lambda s: s["sharpe_ratio"] <= 0.3, "signal": "REDUCE", "score": -1},
]


def generate_recommendation(tickers, weights, stats, investment_amount, risk_level, time_horizon):
    profile = RISK_PROFILES[risk_level]
    allocation = _build_allocation(tickers, weights, investment_amount)
    projected = _project_value(investment_amount, stats["expected_return"], time_horizon)
    sentiment = _assess_sentiment(stats)
    alerts = _generate_alerts(stats, risk_level, profile)
    rebalance = _rebalance_schedule(risk_level, time_horizon)

    return {
        "profile": {
            "risk_level": risk_level,
            "label": profile["label"],
            "description": profile["description"],
        },
        "allocation": allocation,
        "portfolio_stats": stats,
        "projection": projected,
        "sentiment": sentiment,
        "alerts": alerts,
        "rebalance_schedule": rebalance,
        "investment_amount": investment_amount,
        "time_horizon_months": time_horizon,
    }


def _build_allocation(tickers, weights, investment):
    return [
        {
            "ticker": t,
            "weight_pct": round(float(w) * 100, 2),
            "dollar_amount": round(float(w) * investment, 2),
        }
        for t, w in sorted(zip(tickers, weights), key=lambda x: -x[1])
    ]


def _project_value(principal, annual_return, months):
    t = months / 12
    optimistic = principal * (1 + annual_return * 1.3) ** t
    base = principal * (1 + annual_return) ** t
    pessimistic = principal * (1 + annual_return * 0.6) ** t
    return {
        "months": months,
        "optimistic": round(optimistic, 2),
        "base": round(base, 2),
        "pessimistic": round(pessimistic, 2),
        "total_return_pct": round((base / principal - 1) * 100, 2),
    }


def _assess_sentiment(stats):
    for rule in SENTIMENT_RULES:
        if rule["condition"](stats):
            return {
                "signal": rule["signal"],
                "score": rule["score"],
                "rationale": f"Sharpe ratio {stats['sharpe_ratio']:.2f} | Vol {stats['volatility']:.1%}",
            }
    return {"signal": "NEUTRAL", "score": 0, "rationale": "Insufficient signal strength"}


def _generate_alerts(stats, risk_level, profile):
    alerts = []
    if stats["volatility"] > profile["max_volatility"]:
        alerts.append({
            "type": "WARNING",
            "message": f"Portfolio volatility {stats['volatility']:.1%} exceeds {risk_level} risk threshold {profile['max_volatility']:.1%}",
        })
    if stats["sharpe_ratio"] < 0.5:
        alerts.append({
            "type": "INFO",
            "message": "Low Sharpe ratio — consider adding defensive assets or increasing diversification.",
        })
    if stats["max_drawdown"] < -0.3:
        alerts.append({
            "type": "DANGER",
            "message": f"Historical max drawdown {stats['max_drawdown']:.1%}. High downside risk detected.",
        })
    if not alerts:
        alerts.append({"type": "OK", "message": "Portfolio within acceptable risk parameters."})
    return alerts


def _rebalance_schedule(risk_level, time_horizon):
    freq = {"low": "Quarterly", "medium": "Monthly", "high": "Bi-weekly"}
    return {
        "frequency": freq[risk_level],
        "next_review_months": {"low": 3, "medium": 1, "high": 0.5}[risk_level],
    }
