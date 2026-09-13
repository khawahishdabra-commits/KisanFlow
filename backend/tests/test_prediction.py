from app.services.prediction import PredictionService


def test_predict_eta():
    eta = PredictionService.predict_eta(
        queue_length=30,
        avg_service_time=10,
        active_units=2,
    )

    assert eta == 150.0


def test_predict_eta_with_context():
    eta = PredictionService.predict_eta(
        queue_length=30,
        avg_service_time=10,
        active_units=2,
        weather_factor=1.10,
        workload_factor=1.05,
        resource_factor=1.0,
    )

    assert eta == 173.25


def test_predict_eta_without_active_units():
    eta = PredictionService.predict_eta(
        queue_length=30,
        avg_service_time=10,
        active_units=0,
    )

    assert eta == float("inf")


def test_low_congestion():
    result = PredictionService.predict_congestion(
        queue_length=10,
        capacity_per_hour=30,
    )

    assert result == "LOW"


def test_moderate_congestion():
    result = PredictionService.predict_congestion(
        queue_length=18,
        capacity_per_hour=30,
    )

    assert result == "MODERATE"


def test_high_congestion():
    result = PredictionService.predict_congestion(
        queue_length=27,
        capacity_per_hour=30,
    )

    assert result == "HIGH"


def test_critical_congestion():
    result = PredictionService.predict_congestion(
        queue_length=35,
        capacity_per_hour=30,
    )

    assert result == "CRITICAL"

def test_predict_workload():
    workload = PredictionService.predict_workload(
        current_bookings=35,
        expected_walk_ins=15,
        historical_average=20,
    )

    assert workload == 70.0


def test_predict_workload_with_context():
    workload = PredictionService.predict_workload(
        current_bookings=35,
        expected_walk_ins=15,
        historical_average=20,
        context_factor=1.10,
    )

    assert workload == 77.0


def test_predict_workload_with_lower_context():
    workload = PredictionService.predict_workload(
        current_bookings=40,
        expected_walk_ins=10,
        historical_average=20,
        context_factor=0.90,
    )

    assert workload == 63.0


def test_predict_workload_rejects_negative_values():
    try:
        PredictionService.predict_workload(
            current_bookings=-1,
            expected_walk_ins=10,
            historical_average=20,
        )
        assert False
    except ValueError:
        assert True


def test_predict_workload_rejects_invalid_context_factor():
    try:
        PredictionService.predict_workload(
            current_bookings=10,
            expected_walk_ins=10,
            historical_average=10,
            context_factor=0,
        )
        assert False
    except ValueError:
        assert True

def test_predict_eta_with_heavy_rain():
    eta = PredictionService.predict_eta(
        queue_length=20,
        avg_service_time=10,
        active_units=2,
        weather_factor=1.25,
    )

    assert eta == 125.0