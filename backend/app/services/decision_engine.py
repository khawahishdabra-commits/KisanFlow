from dataclasses import dataclass


@dataclass
class CentreDecisionInput:
    centre_id: int
    centre_name: str
    buy_price: float
    eta_minutes: float
    congestion_level: str
    distance_km: float
    travel_cost: float
    weather_score: float


@dataclass
class CentreDecision:
    centre_id: int
    centre_name: str
    score: float
    expected_net_return: float
    reason: str


class DecisionEngine:

    PRICE_WEIGHT = 0.30
    WAIT_WEIGHT = 0.20
    DISTANCE_WEIGHT = 0.15
    CONGESTION_WEIGHT = 0.15
    TRAVEL_WEIGHT = 0.10
    WEATHER_WEIGHT = 0.10

    WAITING_COST_PER_MINUTE = 2.0

    CONGESTION_SCORES = {
        "LOW": 100.0,
        "MODERATE": 75.0,
        "HIGH": 50.0,
        "CRITICAL": 20.0,
    }

    @staticmethod
    def _higher_is_better(
        value: float,
        maximum: float,
    ) -> float:

        if maximum <= 0:
            return 100.0

        return round(
            (value / maximum) * 100,
            2,
        )

    @staticmethod
    def _lower_is_better(
        value: float,
        minimum: float,
    ) -> float:

        if value <= 0:
            return 100.0

        if minimum <= 0:
            return 100.0

        return round(
            (minimum / value) * 100,
            2,
        )

    @classmethod
    def calculate_score(
        cls,
        price_score: float,
        wait_score: float,
        distance_score: float,
        congestion_score: float,
        travel_score: float,
        weather_score: float,
    ) -> float:

        score = (
            price_score * cls.PRICE_WEIGHT
            + wait_score * cls.WAIT_WEIGHT
            + distance_score * cls.DISTANCE_WEIGHT
            + congestion_score * cls.CONGESTION_WEIGHT
            + travel_score * cls.TRAVEL_WEIGHT
            + weather_score * cls.WEATHER_WEIGHT
        )

        return round(score, 2)

    @classmethod
    def rank_centres(
        cls,
        centres: list[CentreDecisionInput],
        quantity: float,
    ) -> list[CentreDecision]:

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        if not centres:
            return []

        highest_price = max(
            centre.buy_price
            for centre in centres
        )

        lowest_wait = min(
            centre.eta_minutes
            for centre in centres
        )

        lowest_distance = min(
            centre.distance_km
            for centre in centres
        )

        lowest_travel_cost = min(
            centre.travel_cost
            for centre in centres
        )

        decisions = []

        for centre in centres:

            price_score = cls._higher_is_better(
                centre.buy_price,
                highest_price,
            )

            wait_score = cls._lower_is_better(
                centre.eta_minutes,
                lowest_wait,
            )

            distance_score = cls._lower_is_better(
                centre.distance_km,
                lowest_distance,
            )

            travel_score = cls._lower_is_better(
                centre.travel_cost,
                lowest_travel_cost,
            )

            congestion_score = cls.CONGESTION_SCORES.get(
                centre.congestion_level.upper(),
                50.0,
            )

            weather_score = max(
                0.0,
                min(100.0, centre.weather_score),
            )

            final_score = cls.calculate_score(
                price_score=price_score,
                wait_score=wait_score,
                distance_score=distance_score,
                congestion_score=congestion_score,
                travel_score=travel_score,
                weather_score=weather_score,
            )

            waiting_cost = (
                centre.eta_minutes
                * cls.WAITING_COST_PER_MINUTE
            )

            expected_net_return = (
                quantity * centre.buy_price
                - centre.travel_cost
                - waiting_cost
            )

            reason = cls._build_reason(
                centre=centre,
                highest_price=highest_price,
                lowest_wait=lowest_wait,
            )

            decisions.append(
                CentreDecision(
                    centre_id=centre.centre_id,
                    centre_name=centre.centre_name,
                    score=final_score,
                    expected_net_return=round(
                        expected_net_return,
                        2,
                    ),
                    reason=reason,
                )
            )

        return sorted(
            decisions,
            key=lambda decision: decision.score,
            reverse=True,
        )

    @staticmethod
    def _build_reason(
        centre: CentreDecisionInput,
        highest_price: float,
        lowest_wait: float,
    ) -> str:

        reasons = []

        if centre.buy_price == highest_price:
            reasons.append("best price")

        if centre.eta_minutes == lowest_wait:
            reasons.append("lowest waiting time")

        if centre.congestion_level.upper() == "LOW":
            reasons.append("low congestion")
        elif centre.congestion_level.upper() == "MODERATE":
            reasons.append("moderate congestion")

        if not reasons:
            reasons.append("balanced price, wait and congestion")

        return "Recommended because of " + ", ".join(reasons)