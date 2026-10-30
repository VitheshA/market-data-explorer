"""Diagnostic for quantstats issue #571: sub-$1 price/return autodetection.

This is an investigation, NOT a proposed upstream fix. The maintainers have
not yet agreed on whether QuantStats should accept price inputs or returns only.
"""
import numpy as np
import pandas as pd


def sample_prices() -> pd.Series:
    dates = pd.date_range("2025-01-02", periods=250, freq="B")
    i = np.arange(len(dates), dtype=float)
    returns = 0.002 + np.sin(i / 13) * 0.012
    prices = pd.Series(0.4 * np.cumprod(1 + returns), index=dates, name="sub_dollar_price")
    return prices * (0.6 / prices.max())


def heuristic_makes_different_choice(s: pd.Series) -> bool:
    """Mirror the condition reported in quantstats utils.py; verify upstream."""
    return bool((s.min() >= 0) and (s.max() > 1))


def diagnostic() -> dict[str, float | bool]:
    low = sample_prices()
    higher = low * 10
    true_returns = low.pct_change().dropna()
    result = {
        "max_low_price": float(low.max()),
        "low_is_detected_as_prices": heuristic_makes_different_choice(low),
        "high_is_detected_as_prices": heuristic_makes_different_choice(higher),
        "true_daily_volatility": float(true_returns.std()),
        "naive_low_level_volatility": float(low.std()),
    }
    return result


if __name__ == "__main__":
    print("QuantStats price/returns ambiguity: one underlying price path, two units")
    print(diagnostic())
    try:
        import quantstats as qs
    except ImportError:
        print("QuantStats not installed. Install it to run the upstream reproduction.")
        raise SystemExit(2)
    prices = sample_prices()
    scaled = prices * 10
    returns = prices.pct_change().dropna()
    print("QuantStats version:", getattr(qs, "__version__", "unknown"))
    print("Sharpe on prices below $1:", qs.stats.sharpe(prices))
    print("Sharpe on equivalent scaled prices:", qs.stats.sharpe(scaled))
    print("Sharpe on explicit daily returns:", qs.stats.sharpe(returns))
    print("Do not propose an automatic fix until the maintainers clarify the input contract.")
