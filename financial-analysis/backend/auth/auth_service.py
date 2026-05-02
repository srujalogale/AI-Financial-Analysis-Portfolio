from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from database.models import User, Portfolio
from auth.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def register_user(db: Session, name: str, email: str, password: str) -> dict:
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = User(name=name, email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email}}


def login_user(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email}}


def get_current_user(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def save_portfolio(db: Session, user_id: int, data: dict) -> Portfolio:
    portfolio = Portfolio(
        user_id=user_id,
        name=data.get("name", "My Portfolio"),
        tickers=data["tickers"],
        risk_level=data["risk_level"],
        investment_amount=data["investment_amount"],
        time_horizon=data.get("time_horizon", 12),
        allocation=data.get("allocation"),
        expected_return=data.get("expected_return"),
        volatility=data.get("volatility"),
        sharpe_ratio=data.get("sharpe_ratio"),
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def get_portfolio_history(db: Session, user_id: int) -> list:
    portfolios = db.query(Portfolio).filter(
        Portfolio.user_id == user_id
    ).order_by(Portfolio.created_at.desc()).all()

    return [{
        "id": p.id,
        "name": p.name,
        "tickers": p.tickers,
        "risk_level": p.risk_level,
        "investment_amount": p.investment_amount,
        "time_horizon": p.time_horizon,
        "allocation": p.allocation,
        "expected_return": p.expected_return,
        "volatility": p.volatility,
        "sharpe_ratio": p.sharpe_ratio,
        "created_at": p.created_at.isoformat(),
    } for p in portfolios]