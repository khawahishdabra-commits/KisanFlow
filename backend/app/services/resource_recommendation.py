from dataclasses import dataclass


@dataclass
class ResourceRecommendation:
    resource_type: str
    recommended_change: int
    reason: str


class ResourceRecommendationService:

    QUEUE_THRESHOLD = 30
    ETA_THRESHOLD = 120

    @classmethod
    def recommend(
        cls,
        queue_length: int,
        eta_minutes: float,
        resources: list,
    ) -> ResourceRecommendation | None:

        if queue_length < 0:
            raise ValueError(
                "Queue length cannot be negative"
            )

        if eta_minutes < 0:
            raise ValueError(
                "ETA cannot be negative"
            )

        if (
            queue_length < cls.QUEUE_THRESHOLD
            and eta_minutes < cls.ETA_THRESHOLD
        ):
            return None

        for resource in resources:

            if resource.resource_type == "Weighing Machine":

                return ResourceRecommendation(
                    resource_type="Weighing Machine",
                    recommended_change=1,
                    reason=(
                        "Queue and predicted waiting time are high. "
                        "Add 1 weighing machine to increase processing capacity."
                    ),
                )

        return ResourceRecommendation(
            resource_type="Processing Unit",
            recommended_change=1,
            reason=(
                "Queue and predicted waiting time are high. "
                "Add 1 processing unit to increase capacity."
            ),
        )