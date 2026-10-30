"""Reusable calculations for the P1 stock explorer. No data downloads here."""
import numpy as np
import pandas as pd


def validate_close(close: pd.Series, label: str) -> pd.Series:
    """Require a sorted positive, numeric price series (adjusted close preferred)."""
    if not isinstance(close, pd.Series):
        raise TypeError(f"{label}: expected pandas Series")
    s = pd.to_numeric(close, errors="coerce").dropna().sort_index()
    if s.empty or len(s) < 3 or (s <= 0).any() or s.index.has_duplicates:
        raise ValueError(f"{label}: need at least 3 positive unique daily closes")
    return s


def align_growth(stock: pd.Series, benchmark: pd.Series, initial: float = 10_000) -> pd.DataFrame:
    """Normalize both prices on their first common trading day."""
    if initial <= 0:
        raise ValueError("initial investment must be positive")
    stock = validate_close(stock, "stock")
    benchmark = validate_close(benchmark, "benchmark")
    joined = pd.concat([stock.rename("Stock"), benchmark.rename("SPY")], axis=1, join="inner").dropna()
    if len(joined) < 3:
        raise ValueError("Not enough overlapping dates")
    return joined.div(joined.iloc[0]).mul(initial)


def summary_metrics(close: pd.Series) -> dict[str, float]:
    close = validate_close(close, "price")
    daily = close.pct_change().dropna()
    years = (close.index[-1] - close.index[0]).days / 365.25
    if years <= 0:
        raise ValueError("Dates must span a positive period")
    wealth = close / close.iloc[0]
    annual_vol = float(daily.std(ddof=1) * np.sqrt(252)) if len(daily) > 1 else float("nan")
    return {
        "total_return": float(close.iloc[-1] / close.iloc[0] - 1),
        "cagr": float((close.iloc[-1] / close.iloc[0]) ** (1 / years) - 1),
        "annual_volatility": annual_vol,
        "max_drawdown": float((wealth / wealth.cummax() - 1).min()),
    }


def rolling_annual_volatility(close: pd.Series, days: int = 30) -> pd.Series:
    if days < 2:
        raise ValueError("days must be at least 2")
    returns = validate_close(close, "price").pct_change()
    return returns.rolling(days).std() * np.sqrt(252)
