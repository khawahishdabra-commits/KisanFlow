from app.services.resource_recommendation import (
    ResourceRecommendationService,
)


class FakeResource:

    def __init__(self, resource_type):
        self.resource_type = resource_type


def test_recommends_weighing_machine_when_pressure_is_high():

    resources = [
        FakeResource("Weighing Machine")
    ]

    result = ResourceRecommendationService.recommend(
        queue_length=35,
        eta_minutes=175,
        resources=resources,
    )

    assert result is not None
    assert result.resource_type == "Weighing Machine"
    assert result.recommended_change == 1


def test_no_recommendation_when_centre_is_healthy():

    resources = [
        FakeResource("Weighing Machine")
    ]

    result = ResourceRecommendationService.recommend(
        queue_length=10,
        eta_minutes=40,
        resources=resources,
    )

    assert result is None


def test_recommends_processing_unit_when_no_weighing_machine():

    resources = [
        FakeResource("Storage Unit")
    ]

    result = ResourceRecommendationService.recommend(
        queue_length=40,
        eta_minutes=150,
        resources=resources,
    )

    assert result is not None
    assert result.resource_type == "Processing Unit"


def test_negative_queue_is_rejected():

    try:
        ResourceRecommendationService.recommend(
            queue_length=-1,
            eta_minutes=100,
            resources=[],
        )
        assert False
    except ValueError:
        assert True


def test_negative_eta_is_rejected():

    try:
        ResourceRecommendationService.recommend(
            queue_length=30,
            eta_minutes=-1,
            resources=[],
        )
        assert False
    except ValueError:
        assert True