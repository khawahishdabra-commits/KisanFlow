from datetime import date

from app.models.centre import Centre
from app.models.price import Price
from app.models.queue import Queue
from app.models.resource import Resource
from app.schemas.recommendation import (
    LocationInput,
    RecommendationRequest,
)
from app.services.recommendation import RecommendationService


class FakeCentreRepository:

    def get_all(self):

        return [
            Centre(
                id=1,
                name="Centre A",
                address="Location A",
                latitude=30.40,
                longitude=76.82,
                status="ACTIVE",
                capacity_per_hour=30,
            ),
            Centre(
                id=2,
                name="Centre B",
                address="Location B",
                latitude=30.41,
                longitude=76.80,
                status="ACTIVE",
                capacity_per_hour=25,
            ),
            Centre(
                id=3,
                name="Centre C",
                address="Location C",
                latitude=30.45,
                longitude=76.85,
                status="ACTIVE",
                capacity_per_hour=35,
            ),
        ]


class FakePriceRepository:

    def get_prices_for_crop(self, crop_id):

        return [
            Price(
                id=1,
                centre_id=1,
                crop_id=crop_id,
                buy_price=2400,
                sell_price=2500,
                effective_date=date.today(),
            ),
            Price(
                id=2,
                centre_id=2,
                crop_id=crop_id,
                buy_price=2350,
                sell_price=2450,
                effective_date=date.today(),
            ),
            Price(
                id=3,
                centre_id=3,
                crop_id=crop_id,
                buy_price=2450,
                sell_price=2550,
                effective_date=date.today(),
            ),
        ]


class FakeIntelligenceRepository:

    def get_queue(self, centre_id):

        queues = {
            1: Queue(
                centre_id=1,
                queue_length=35,
                avg_service_time=10,
                estimated_wait_minutes=105,
            ),
            2: Queue(
                centre_id=2,
                queue_length=12,
                avg_service_time=8,
                estimated_wait_minutes=38.4,
            ),
            3: Queue(
                centre_id=3,
                queue_length=20,
                avg_service_time=7,
                estimated_wait_minutes=28,
            ),
        }

        return queues.get(centre_id)

    def get_resources(self, centre_id):

        return [
            Resource(
                centre_id=centre_id,
                resource_type="Weighing Machine",
                total_units=3,
                available_units=2,
                status="AVAILABLE",
            )
        ]


def test_recommendation_service():

    service = RecommendationService(
        centre_repository=FakeCentreRepository(),
        price_repository=FakePriceRepository(),
        intelligence_repository=FakeIntelligenceRepository(),
    )

    request = RecommendationRequest(
        crop_id=1,
        quantity=25,
        location=LocationInput(
            lat=30.37,
            lon=76.78,
        ),
    )

    result = service.recommend(request)

    assert result.recommended_centre is not None

    assert result.recommended_centre.id > 0

    assert result.recommended_centre.score > 0

    assert result.recommended_centre.expected_net_return > 0

    assert len(result.alternatives) == 2


def test_recommendation_contains_reason():

    service = RecommendationService(
        centre_repository=FakeCentreRepository(),
        price_repository=FakePriceRepository(),
        intelligence_repository=FakeIntelligenceRepository(),
    )

    request = RecommendationRequest(
        crop_id=1,
        quantity=25,
        location=LocationInput(
            lat=30.37,
            lon=76.78,
        ),
    )

    result = service.recommend(request)

    assert result.recommended_centre.reason


def test_recommendation_has_ranked_alternatives():

    service = RecommendationService(
        centre_repository=FakeCentreRepository(),
        price_repository=FakePriceRepository(),
        intelligence_repository=FakeIntelligenceRepository(),
    )

    request = RecommendationRequest(
        crop_id=1,
        quantity=25,
        location=LocationInput(
            lat=30.37,
            lon=76.78,
        ),
    )

    result = service.recommend(request)

    scores = [
        result.recommended_centre.score
    ]

    scores.extend(
        alternative.score
        for alternative in result.alternatives
    )

    assert scores == sorted(
        scores,
        reverse=True,
    )

def test_recommendation_excludes_centre_with_no_active_units():

    class ZeroCapacityIntelligenceRepository(
        FakeIntelligenceRepository
    ):

        def get_resources(self, centre_id):

            if centre_id == 3:
                return [
                    Resource(
                        centre_id=centre_id,
                        resource_type="Weighing Machine",
                        total_units=3,
                        available_units=0,
                        status="AVAILABLE",
                    )
                ]

            return super().get_resources(centre_id)

    service = RecommendationService(
        centre_repository=FakeCentreRepository(),
        price_repository=FakePriceRepository(),
        intelligence_repository=ZeroCapacityIntelligenceRepository(),
    )

    request = RecommendationRequest(
        crop_id=1,
        quantity=25,
        location=LocationInput(
            lat=30.37,
            lon=76.78,
        ),
    )

    result = service.recommend(request)

    centre_ids = [
        result.recommended_centre.id
    ]

    centre_ids.extend(
        alternative.id
        for alternative in result.alternatives
    )

    assert 3 not in centre_ids