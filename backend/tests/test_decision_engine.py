from app.services.decision_engine import (
    CentreDecisionInput,
    DecisionEngine,
)


def test_rank_centres_returns_highest_score_first():

    centres = [
        CentreDecisionInput(
            centre_id=1,
            centre_name="Centre A",
            buy_price=2400,
            eta_minutes=175,
            congestion_level="CRITICAL",
            distance_km=8,
            travel_cost=160,
            weather_score=100,
        ),
        CentreDecisionInput(
            centre_id=2,
            centre_name="Centre B",
            buy_price=2350,
            eta_minutes=60,
            congestion_level="MODERATE",
            distance_km=5,
            travel_cost=100,
            weather_score=100,
        ),
        CentreDecisionInput(
            centre_id=3,
            centre_name="Centre C",
            buy_price=2450,
            eta_minutes=40,
            congestion_level="LOW",
            distance_km=12,
            travel_cost=240,
            weather_score=80,
        ),
    ]

    results = DecisionEngine.rank_centres(
        centres=centres,
        quantity=25,
    )

    assert len(results) == 3

    assert results[0].score >= results[1].score
    assert results[1].score >= results[2].score


def test_expected_net_return():

    centre = CentreDecisionInput(
        centre_id=1,
        centre_name="Centre A",
        buy_price=2400,
        eta_minutes=100,
        congestion_level="MODERATE",
        distance_km=5,
        travel_cost=100,
        weather_score=100,
    )

    results = DecisionEngine.rank_centres(
        centres=[centre],
        quantity=25,
    )

    expected_return = (
        25 * 2400
        - 100
        - (100 * 2)
    )

    assert results[0].expected_net_return == expected_return


def test_empty_centres():

    results = DecisionEngine.rank_centres(
        centres=[],
        quantity=25,
    )

    assert results == []


def test_invalid_quantity():

    try:
        DecisionEngine.rank_centres(
            centres=[],
            quantity=0,
        )
        assert False
    except ValueError:
        assert True


def test_recommendation_reason_is_generated():

    centre = CentreDecisionInput(
        centre_id=1,
        centre_name="Centre A",
        buy_price=2500,
        eta_minutes=30,
        congestion_level="LOW",
        distance_km=5,
        travel_cost=100,
        weather_score=100,
    )

    results = DecisionEngine.rank_centres(
        centres=[centre],
        quantity=25,
    )

    assert "best price" in results[0].reason
    assert "lowest waiting time" in results[0].reason
    assert "low congestion" in results[0].reason