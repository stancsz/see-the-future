import pytest
from see_the_future.core import Scenario, Event

def test_independent_event_creation():
    event = Event("Test Event", 0.5)
    assert event.name == "Test Event"
    assert event.probability == 0.5
    assert not event.is_conditional
    assert len(event.parent_events) == 0

def test_conditional_event_creation():
    event = Event("Child Event", 0.0)
    event.make_conditional("Parent Event", 0.8, 0.2)
    assert event.is_conditional
    assert event.parent_events == ["Parent Event"]
    assert event.conditions == {"1": 0.8, "0": 0.2}

def test_multi_conditional_event_creation():
    event = Event("Child Event", 0.0)
    probs = {"00": 0.1, "01": 0.2, "10": 0.3, "11": 0.4}
    event.make_multi_conditional(["P1", "P2"], probs)
    assert event.is_conditional
    assert event.parent_events == ["P1", "P2"]
    assert event.conditions == probs

def test_scenario_add_independent():
    scenario = Scenario("Test Scenario")
    event = scenario.add_independent_event("A", 0.5)
    assert "A" in scenario.events
    assert scenario.event_order == ["A"]
    assert scenario.get_event_index("A") == 0

def test_scenario_add_conditional():
    scenario = Scenario("Test Scenario")
    scenario.add_independent_event("A", 0.5)
    scenario.add_conditional_event("B", "A", 0.8, 0.2)
    assert "B" in scenario.events
    assert scenario.event_order == ["A", "B"]
    assert scenario.get_event_index("B") == 1

def test_scenario_add_multi_conditional():
    scenario = Scenario("Test Scenario")
    scenario.add_independent_event("A", 0.5)
    scenario.add_independent_event("B", 0.5)
    scenario.add_multi_conditional_event("C", ["A", "B"], {"00": 0.1, "01": 0.2, "10": 0.3, "11": 0.4})
    assert "C" in scenario.events
    assert scenario.event_order == ["A", "B", "C"]
    assert scenario.get_event_index("C") == 2

def test_scenario_duplicate_event_error():
    scenario = Scenario("Test Scenario")
    scenario.add_independent_event("A", 0.5)
    with pytest.raises(ValueError):
        scenario.add_independent_event("A", 0.6)

def test_scenario_missing_parent_error():
    scenario = Scenario("Test Scenario")
    with pytest.raises(ValueError):
        scenario.add_conditional_event("B", "A", 0.8, 0.2)

def test_scenario_missing_multi_parent_error():
    scenario = Scenario("Test Scenario")
    scenario.add_independent_event("A", 0.5)
    with pytest.raises(ValueError):
        scenario.add_multi_conditional_event("C", ["A", "B"], {"00": 0.1, "01": 0.2, "10": 0.3, "11": 0.4})
