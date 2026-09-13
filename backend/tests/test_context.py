from app.services.context import ContextService


def test_clear_weather_score():
    assert ContextService.get_weather_score("CLEAR") == 100.0


def test_heavy_rain_weather_score():
    assert ContextService.get_weather_score("HEAVY_RAIN") == 40.0


def test_clear_weather_factor():
    assert ContextService.get_weather_factor("CLEAR") == 1.00


def test_heavy_rain_weather_factor():
    assert ContextService.get_weather_factor("HEAVY_RAIN") == 1.25


def test_unknown_weather_condition_uses_safe_defaults():
    assert ContextService.get_weather_score("UNKNOWN") == 70.0
    assert ContextService.get_weather_factor("UNKNOWN") == 1.10