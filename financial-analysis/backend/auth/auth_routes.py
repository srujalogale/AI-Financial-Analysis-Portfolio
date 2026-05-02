from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from database.db import get_db
from auth.auth_service import register_user, login_user, get_current_user, save_portfolio, get_portfolio_history
from auth.jwt_handler import verify_token_email

router = APIRouter()
bearer = HTTPBearer()


# ── Request schemas ───────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SavePortfolioRequest(BaseModel):
    name: str = "My Portfolio"
    tickers: list[str]
    risk_level: str = "medium"
    investment_amount: float = 10000.0
    time_horizon: int = 12
    allocation: list | None = None
    expected_return: float | None = None
    volatility: float | None = None
    sharpe_ratio: float | None = None


# ── Dependency: get current user from token ───────────────────────────────────
def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    email = verify_token_email(credentials.credentials)
    return get_current_user(db, email)


# ── Auth Routes ───────────────────────────────────────────────────────────────
@router.post("/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(db, req.name, req.email, req.password)


@router.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, req.email, req.password)


# ── User Routes ───────────────────────────────────────────────────────────────
@router.get("/user/profile")
def profile(user=Depends(get_authenticated_user)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "portfolio_count": len(user.portfolios),
    }


# ── Portfolio Save/History ────────────────────────────────────────────────────
@router.post("/portfolio/save")
def save(req: SavePortfolioRequest, user=Depends(get_authenticated_user), db: Session = Depends(get_db)):
    p = save_portfolio(db, user.id, req.model_dump())
    return {"message": "Portfolio saved", "portfolio_id": p.id, "created_at": p.created_at.isoformat()}


@router.get("/portfolio/history")
def history(user=Depends(get_authenticated_user), db: Session = Depends(get_db)):
    return get_portfolio_history(db, user.id)