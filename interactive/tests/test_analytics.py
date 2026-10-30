import numpy as np
import pandas as pd
import pytest
from analytics import align_growth, summary_metrics, rolling_annual_volatility


def test_equal_growth_for_equal_scaled_prices():
    dates = pd.date_range("2024-01-02", periods=70, freq="B")
    s = pd.Series(np.linspace(10.0, 20.0, len(dates)), index=dates)
    g = align_growth(s, s * 3)
    assert np.allclose(g.Stock, g.SPY)
    assert g.iloc[0].tolist() == [10_000, 10_000]


def test_max_drawdown_first_day():
    dates = pd.date_range("2024-01-02", periods=5, freq="B")
    s = pd.Series([100., 90., 95., 95., 110.], index=dates)
    assert summary_metrics(s)["max_drawdown"] == pytest.approx(-0.10)


def test_reject_nonpositive_prices():
    s = pd.Series([1., 0., 2.], index=pd.date_range("2024-01-02", periods=3))
    with pytest.raises(ValueError):
        summary_metrics(s)


def test_vol_window():
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    vol = rolling_annual_volatility(pd.Series(range(1,11), index=dates, dtype=float), days=4)
    assert vol.notna().sum() == 6
