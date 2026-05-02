from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class MarketDataRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    period: str = "1y"


class RecommendRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL", "AMZN", "BTC-USD"]
    investment_amount: float = Field(default=10000.0, gt=0)
    risk_level: Literal["low", "medium", "high"] = "medium"
    time_horizon: int = Field(default=12, ge=1, le=120)
    period: str = "2y"


class SimulateRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL", "AMZN", "BTC-USD"]
    investment_amount: float = Field(default=10000.0, gt=0)
    risk_level: Literal["low", "medium", "high"] = "medium"
    days: int = Field(default=252, ge=30, le=1260)
    simulations: int = Field(default=1000, ge=100, le=5000)
    period: str = "2y"


class LiveQuoteRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL"]


class IntradayRequest(BaseModel):
    ticker: str = "AAPL"
    interval: Literal["1m", "5m", "15m", "30m", "1h"] = "5m"


class PredictRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT"]
    days_ahead: int = Field(default=7, ge=1, le=30)
    period: str = "2y"


class TechnicalRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL"]
    period: str = "1y"


class SentimentRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT"]


class PortfolioHolding(BaseModel):
    ticker: str
    shares: float = Field(gt=0)
    avg_cost: float = Field(gt=0)


class PortfolioTrackRequest(BaseModel):
    holdings: List[PortfolioHolding]


class CompareRequest(BaseModel):
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL"]
    period: str = "1y"


class ScreenerRequest(BaseModel):
    min_return: float = 0.05
    max_volatility: float = 0.40
    min_sharpe: float = 0.5
    universe: Optional[List[str]] = None
    period: str = "1y"
    top_n: int = Field(default=10, ge=1, le=50)


class AlertRequest(BaseModel):
    ticker: str = "AAPL"
    price_target: Optional[float] = None
    stop_loss: Optional[float] = None
