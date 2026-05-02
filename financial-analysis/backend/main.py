from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from auth.auth_routes import router as auth_router

from models.schemas import (
    RecommendRequest, SimulateRequest, MarketDataRequest,
    LiveQuoteRequest, IntradayRequest, PredictRequest, TechnicalRequest,
    SentimentRequest, PortfolioTrackRequest, CompareRequest, ScreenerRequest, AlertRequest
)
from services.data_service import fetch_market_data
from services.risk_service import compute_risk_metrics
from services.optimization_service import optimize_portfolio
from services.simulation_service import run_monte_carlo
from services.recommendation_service import generate_recommendation
from services.live_data_service import get_live_quote, get_intraday, get_multi_quotes
from services.technical_service import compute_all_indicators
from services.prediction_service import predict_prices
from services.sentiment_service import analyze_sentiment
from services.portfolio_tracker_service import analyze_portfolio, compare_stocks
from services.screener_service import screen_stocks
from services.alerts_service import check_alerts

app = FastAPI(title="AI Portfolio System", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init DB on startup
@app.on_event("startup")
def startup():
    init_db()

# Auth + User + Portfolio save/history routes
app.include_router(auth_router)


def safe(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health(): return {"status": "ok", "version": "3.0.0"}


# ── Market Data ───────────────────────────────────────────────────────────────
@app.post("/market/data")
def market_data(req: MarketDataRequest):
    def _():
        df = fetch_market_data(req.tickers, req.period)
        returns = df.pct_change().dropna()
        valid = [t for t in req.tickers if t in df.columns]
        metrics = {t: compute_risk_metrics(returns[t]) for t in valid}
        return {
            "tickers": valid,
            "prices": {t: df[t].dropna().tail(60).tolist() for t in valid},
            "dates": [str(d.date()) for d in df.dropna().tail(60).index],
            "metrics": metrics,
        }
    return safe(_)


@app.post("/market/live")
def live_quotes(req: LiveQuoteRequest):
    return safe(get_multi_quotes, req.tickers)


@app.post("/market/intraday")
def intraday(req: IntradayRequest):
    return safe(get_intraday, req.ticker, req.interval)


# ── Portfolio ─────────────────────────────────────────────────────────────────
@app.post("/portfolio/recommend")
def recommend(req: RecommendRequest):
    def _():
        df = fetch_market_data(req.tickers, req.period)
        returns = df.pct_change().dropna()
        weights, stats = optimize_portfolio(returns, req.risk_level)
        valid = list(df.columns)
        return generate_recommendation(valid, weights, stats, req.investment_amount, req.risk_level, req.time_horizon)
    return safe(_)


@app.post("/portfolio/simulate")
def simulate(req: SimulateRequest):
    def _():
        df = fetch_market_data(req.tickers, req.period)
        returns = df.pct_change().dropna()
        weights, _ = optimize_portfolio(returns, req.risk_level)
        return run_monte_carlo(returns, weights, req.investment_amount, req.days, req.simulations)
    return safe(_)


@app.post("/portfolio/track")
def track_portfolio(req: PortfolioTrackRequest):
    holdings = [h.model_dump() for h in req.holdings]
    return safe(analyze_portfolio, holdings)


@app.post("/portfolio/compare")
def compare(req: CompareRequest):
    return safe(compare_stocks, req.tickers, req.period)


# ── AI Prediction ─────────────────────────────────────────────────────────────
@app.post("/ai/predict")
def predict(req: PredictRequest):
    def _():
        df = fetch_market_data(req.tickers, req.period)
        return {t: predict_prices(df, t, req.days_ahead) for t in df.columns}
    return safe(_)


# ── Technical Indicators ──────────────────────────────────────────────────────
@app.post("/technical/indicators")
def technical(req: TechnicalRequest):
    def _():
        df = fetch_market_data(req.tickers, req.period)
        return compute_all_indicators(df)
    return safe(_)


# ── Sentiment ─────────────────────────────────────────────────────────────────
@app.post("/sentiment/analyze")
def sentiment(req: SentimentRequest):
    return safe(lambda: {t: analyze_sentiment(t) for t in req.tickers})


# ── Screener ──────────────────────────────────────────────────────────────────
@app.post("/screener/run")
def screener(req: ScreenerRequest):
    return safe(screen_stocks, req.min_return, req.max_volatility, req.min_sharpe,
                req.universe, req.period, req.top_n)


# ── Alerts ────────────────────────────────────────────────────────────────────
@app.post("/alerts/check")
def alerts(req: AlertRequest):
    return safe(check_alerts, req.ticker, req.price_target, req.stop_loss)
