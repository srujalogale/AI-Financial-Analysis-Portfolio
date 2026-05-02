import numpy as np
import pandas as pd


def run_monte_carlo(returns: pd.DataFrame, weights: np.ndarray,
                    investment: float, days: int = 252, simulations: int = 1000) -> dict:
    port_returns = (returns.values @ weights)
    mu = port_returns.mean()
    sigma = port_returns.std()

    rng = np.random.default_rng(42)
    daily = rng.normal(mu, sigma, (simulations, days))
    paths = investment * np.cumprod(1 + daily, axis=1)

    final = paths[:, -1]
    percentiles = [5, 10, 25, 50, 75, 90, 95]
    pct_values = np.percentile(final, percentiles)

    # Sample paths for visualization (20 paths)
    sample_idx = rng.choice(simulations, size=min(20, simulations), replace=False)
    sample_paths = paths[sample_idx].tolist()

    return {
        "investment": investment,
        "days": days,
        "simulations": simulations,
        "percentiles": {str(p): round(float(v), 2) for p, v in zip(percentiles, pct_values)},
        "expected_final": round(float(final.mean()), 2),
        "prob_profit": round(float((final > investment).mean()), 4),
        "prob_loss_20pct": round(float((final < investment * 0.8).mean()), 4),
        "sample_paths": [[round(v, 2) for v in path] for path in sample_paths],
        "summary": {
            "best_case": round(float(final.max()), 2),
            "worst_case": round(float(final.min()), 2),
            "std_dev": round(float(final.std()), 2),
        },
    }
