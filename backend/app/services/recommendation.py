from fastapi import HTTPException

from app.repositories.centre import CentreRepository
from app.repositories.intelligence import IntelligenceRepository
from app.repositories.price import PriceRepository
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedCentre,
    CentreAlternative,
)
from app.services.context import ContextService
from app.services.decision_engine import (
    CentreDecisionInput,
    DecisionEngine,
)
from app.services.distance import DistanceService
from app.services.prediction import PredictionService


class RecommendationService:

    TRAVEL_COST_PER_KM = 20.0

    def __init__(
        self,
        centre_repository: CentreRepository,
        price_repository: PriceRepository,
        intelligence_repository: IntelligenceRepository,
    ):
        self.centre_repository = centre_repository
        self.price_repository = price_repository
        self.intelligence_repository = intelligence_repository

    def recommend(
        self,
        data: RecommendationRequest,
    ) -> RecommendationResponse:

        centres = self.centre_repository.get_all()

        if not centres:
            raise HTTPException(
                status_code=404,
                detail="No procurement centres available",
            )

        prices = self.price_repository.get_prices_for_crop(
            data.crop_id
        )

        if not prices:
            raise HTTPException(
                status_code=404,
                detail="No prices found for this crop",
            )

        price_by_centre = {
            price.centre_id: price
            for price in prices
        }

        # Current demo weather context.
        # Later this can come from a real weather provider.
        weather_condition = "CLEAR"

        weather_score = ContextService.get_weather_score(
            weather_condition
        )

        weather_factor = ContextService.get_weather_factor(
            weather_condition
        )

        decision_inputs = []

        # Store the raw intelligence metrics separately.
        # DecisionEngine is responsible for ranking,
        # while RecommendationService exposes these
        # metrics in the API response.
        decision_metrics = {}

        for centre in centres:

            price = price_by_centre.get(centre.id)

            if not price:
                continue

            queue = self.intelligence_repository.get_queue(
                centre.id
            )

            if not queue:
                continue

            resources = (
                self.intelligence_repository.get_resources(
                    centre.id
                )
            )

            active_units = sum(
                resource.available_units
                for resource in resources
                if resource.status == "AVAILABLE"
            )

            # A centre with no active processing capacity
            # cannot be recommended.
            if active_units <= 0:
                continue

            eta_minutes = PredictionService.predict_eta(
                queue_length=queue.queue_length,
                avg_service_time=queue.avg_service_time,
                active_units=active_units,
                weather_factor=weather_factor,
            )

            congestion_level = (
                PredictionService.predict_congestion(
                    queue_length=queue.queue_length,
                    capacity_per_hour=centre.capacity_per_hour,
                )
            )

            if (
                centre.latitude is None
                or centre.longitude is None
            ):
                continue

            distance_km = (
                DistanceService.calculate_distance_km(
                    latitude1=data.location.lat,
                    longitude1=data.location.lon,
                    latitude2=centre.latitude,
                    longitude2=centre.longitude,
                )
            )

            travel_cost = (
                distance_km
                * self.TRAVEL_COST_PER_KM
            )

            # Preserve the metrics used for the recommendation.
            decision_metrics[centre.id] = {
                "price": price.buy_price,
                "eta_minutes": eta_minutes,
                "congestion": congestion_level,
                "distance_km": distance_km,
            }

            decision_inputs.append(
                CentreDecisionInput(
                    centre_id=centre.id,
                    centre_name=centre.name,
                    buy_price=price.buy_price,
                    eta_minutes=eta_minutes,
                    congestion_level=congestion_level,
                    distance_km=distance_km,
                    travel_cost=travel_cost,
                    weather_score=weather_score,
                )
            )

        if not decision_inputs:
            raise HTTPException(
                status_code=404,
                detail="No centres have sufficient data for recommendation",
            )

        decisions = DecisionEngine.rank_centres(
            centres=decision_inputs,
            quantity=data.quantity,
        )

        recommended = decisions[0]

        recommended_metrics = decision_metrics[
            recommended.centre_id
        ]

        alternatives = [
            CentreAlternative(
                id=decision.centre_id,
                name=decision.centre_name,
                score=decision.score,
                expected_net_return=decision.expected_net_return,
                price=decision_metrics[
                    decision.centre_id
                ]["price"],
                eta_minutes=decision_metrics[
                    decision.centre_id
                ]["eta_minutes"],
                congestion=decision_metrics[
                    decision.centre_id
                ]["congestion"],
                distance_km=decision_metrics[
                    decision.centre_id
                ]["distance_km"],
            )
            for decision in decisions[1:]
        ]

        return RecommendationResponse(
            recommended_centre=RecommendedCentre(
                id=recommended.centre_id,
                name=recommended.centre_name,
                score=recommended.score,
                expected_net_return=recommended.expected_net_return,
                price=recommended_metrics["price"],
                eta_minutes=recommended_metrics["eta_minutes"],
                congestion=recommended_metrics["congestion"],
                distance_km=recommended_metrics["distance_km"],
                reason=recommended.reason,
            ),
            alternatives=alternatives,
        )