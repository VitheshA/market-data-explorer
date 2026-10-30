from reproduce_quantstats_571 import diagnostic, sample_prices


def test_same_path_different_heuristic_choice():
    prices = sample_prices()
    assert 0 < prices.min() < prices.max() <= 0.61
    result = diagnostic()
    assert result["low_is_detected_as_prices"] is False
    assert result["high_is_detected_as_prices"] is True


def test_explicit_return_volatility_is_not_price_volatility():
    result = diagnostic()
    assert abs(result["true_daily_volatility"] - result["naive_low_level_volatility"]) > 0.01
