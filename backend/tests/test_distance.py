from app.services.distance import DistanceService


def test_same_location():

    distance = DistanceService.calculate_distance_km(
        latitude1=30.0,
        longitude1=70.0,
        latitude2=30.0,
        longitude2=70.0,
    )

    assert distance == 0.0


def test_distance_is_positive():

    distance = DistanceService.calculate_distance_km(
        latitude1=30.0,
        longitude1=70.0,
        latitude2=30.1,
        longitude2=70.1,
    )

    assert distance > 0


def test_distance_is_symmetric():

    distance1 = DistanceService.calculate_distance_km(
        latitude1=30.0,
        longitude1=70.0,
        latitude2=30.1,
        longitude2=70.1,
    )

    distance2 = DistanceService.calculate_distance_km(
        latitude1=30.1,
        longitude1=70.1,
        latitude2=30.0,
        longitude2=70.0,
    )

    assert distance1 == distance2