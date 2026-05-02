import yfinance as yf
from datetime import datetime
import re


POSITIVE_WORDS = {
    "surge", "soar", "rally", "gain", "profit", "beat", "exceed", "record", "high",
    "growth", "strong", "upgrade", "buy", "bullish", "rise", "jump", "boost",
    "outperform", "positive", "revenue", "dividend", "expand", "partnership"
}
NEGATIVE_WORDS = {
    "fall", "drop", "plunge", "loss", "miss", "decline", "cut", "downgrade",
    "sell", "bearish", "crash", "weak", "risk", "debt", "layoff", "lawsuit",
    "recall", "fraud", "investigation", "fine", "penalty", "underperform", "warning"
}


def analyze_sentiment(ticker: str) -> dict:
    try:
        t = yf.Ticker(ticker)
        news = t.news or []
    except Exception:
        news = []

    if not news:
        return _empty_sentiment(ticker)

    analyzed = []
    total_score = 0

    for item in news[:15]:
        title = item.get("title", "") or ""
        summary = item.get("summary", "") or ""
        text = (title + " " + summary).lower()
        score, label = _score_text(text)
        total_score += score
        analyzed.append({
            "title": title[:120],
            "sentiment": label,
            "score": score,
            "source": item.get("publisher", "Unknown"),
            "url": item.get("link", ""),
            "published": _fmt_time(item.get("providerPublishTime")),
        })

    n = len(analyzed)
    avg = total_score / n if n else 0
    positive = sum(1 for a in analyzed if a["sentiment"] == "Positive")
    negative = sum(1 for a in analyzed if a["sentiment"] == "Negative")
    neutral = n - positive - negative

    if avg > 0.3: overall = "Bullish"
    elif avg < -0.3: overall = "Bearish"
    else: overall = "Neutral"

    return {
        "ticker": ticker,
        "overall_sentiment": overall,
        "avg_score": round(avg, 3),
        "total_articles": n,
        "positive_count": positive,
        "negative_count": negative,
        "neutral_count": neutral,
        "sentiment_pct": {
            "positive": round(positive / n * 100, 1) if n else 0,
            "negative": round(negative / n * 100, 1) if n else 0,
            "neutral": round(neutral / n * 100, 1) if n else 0,
        },
        "articles": analyzed[:10],
    }


def _score_text(text: str) -> tuple[float, str]:
    words = set(re.findall(r'\b\w+\b', text))
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    score = (pos - neg) / max(pos + neg, 1)
    label = "Positive" if score > 0.1 else "Negative" if score < -0.1 else "Neutral"
    return round(score, 3), label


def _empty_sentiment(ticker: str) -> dict:
    return {
        "ticker": ticker, "overall_sentiment": "Neutral", "avg_score": 0,
        "total_articles": 0, "positive_count": 0, "negative_count": 0, "neutral_count": 0,
        "sentiment_pct": {"positive": 0, "negative": 0, "neutral": 0},
        "articles": [],
    }


def _fmt_time(ts) -> str:
    if not ts: return "N/A"
    try: return datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
    except: return "N/A"
