from utils.config import MAX_TICKERS


def validate_tickers(tickers: list[str]):
    if not tickers:
        raise ValueError("At least one ticker is required.")
    if len(tickers) > MAX_TICKERS:
        raise ValueError(f"Max {MAX_TICKERS} tickers allowed.")
    if len(tickers) < 2:
        raise ValueError("At least 2 tickers required for portfolio optimization.")


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def fmt_currency(value: float) -> str:
    return f"${value:,.2f}"
