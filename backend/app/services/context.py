class ContextService:

    @staticmethod
    def get_weather_score(
        weather_condition: str,
    ) -> float:

        scores = {
            "CLEAR": 100.0,
            "CLOUDY": 90.0,
            "LIGHT_RAIN": 75.0,
            "HEAVY_RAIN": 40.0,
            "STORM": 20.0,
        }

        return scores.get(
            weather_condition.upper(),
            70.0,
        )

    @staticmethod
    def get_weather_factor(
        weather_condition: str,
    ) -> float:

        factors = {
            "CLEAR": 1.00,
            "CLOUDY": 1.05,
            "LIGHT_RAIN": 1.10,
            "HEAVY_RAIN": 1.25,
            "STORM": 1.50,
        }

        return factors.get(
            weather_condition.upper(),
            1.10,
        )