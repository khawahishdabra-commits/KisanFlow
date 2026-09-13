import pytest

from app.services.simulation import SimulationService


def test_simulation_reduces_wait_time():

    result = SimulationService.simulate(
        queue_length=35,
        avg_service_time=10,
        active_units=2,
        resource_type="Weighing Machine",
        resource_change=1,
    )

    assert result.before_queue == 35
    assert result.before_wait == 175
    assert result.after_wait == pytest.approx(116.67, rel=1e-2)
    assert result.after_queue == 23


def test_simulation_resource_information():

    result = SimulationService.simulate(
        queue_length=20,
        avg_service_time=10,
        active_units=2,
        resource_type="Weighing Machine",
        resource_change=1,
    )

    assert result.resource_type == "Weighing Machine"
    assert result.resource_change == 1


def test_negative_queue_rejected():

    with pytest.raises(ValueError):
        SimulationService.simulate(
            queue_length=-1,
            avg_service_time=10,
            active_units=2,
            resource_type="Weighing Machine",
            resource_change=1,
        )


def test_zero_active_units_rejected():

    with pytest.raises(ValueError):
        SimulationService.simulate(
            queue_length=35,
            avg_service_time=10,
            active_units=0,
            resource_type="Weighing Machine",
            resource_change=1,
        )


def test_zero_resource_change_rejected():

    with pytest.raises(ValueError):
        SimulationService.simulate(
            queue_length=35,
            avg_service_time=10,
            active_units=2,
            resource_type="Weighing Machine",
            resource_change=0,
        )