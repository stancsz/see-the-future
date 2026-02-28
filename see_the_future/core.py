from typing import Dict, List, Optional, Tuple, Union

class Event:
    """Represents an event in a scenario."""
    def __init__(self, name: str, probability: float):
        """
        Initialize an independent event.

        Args:
            name: The name of the event.
            probability: The base probability of the event occurring (0.0 to 1.0).
        """
        self.name = name
        self.probability = probability
        self.is_conditional = False
        self.conditions: Dict[str, float] = {}
        # List of parent event names this event depends on
        self.parent_events: List[str] = []

    def make_conditional(self, parent_event: str, prob_if_true: float, prob_if_false: float):
        """
        Make this event conditional on a single parent event.

        Args:
            parent_event: The name of the parent event.
            prob_if_true: The probability of this event occurring if the parent event is True.
            prob_if_false: The probability of this event occurring if the parent event is False.
        """
        self.is_conditional = True
        self.parent_events = [parent_event]
        # For a single parent, state can be "1" (True) or "0" (False)
        self.conditions = {
            "1": prob_if_true,
            "0": prob_if_false
        }

    def make_multi_conditional(self, parent_events: List[str], condition_probs: Dict[str, float]):
        """
        Make this event conditional on multiple parent events.

        Args:
            parent_events: A list of parent event names.
            condition_probs: A dictionary mapping binary state strings (e.g., "10" for true, false)
                             to the probability of this event occurring.
        """
        self.is_conditional = True
        self.parent_events = parent_events
        self.conditions = condition_probs


class Scenario:
    """Defines a scenario consisting of multiple events."""
    def __init__(self, name: str):
        """
        Initialize a new scenario.

        Args:
            name: The name of the scenario.
        """
        self.name = name
        self.events: Dict[str, Event] = {}
        self.event_order: List[str] = []

    def add_independent_event(self, name: str, probability: float) -> Event:
        """
        Add an independent event to the scenario.

        Args:
            name: The name of the event.
            probability: The base probability of the event occurring.

        Returns:
            The created Event object.
        """
        if name in self.events:
            raise ValueError(f"Event '{name}' already exists in the scenario.")

        event = Event(name, probability)
        self.events[name] = event
        self.event_order.append(name)
        return event

    def add_conditional_event(self, name: str, parent_event: str,
                              prob_if_true: float, prob_if_false: float) -> Event:
        """
        Add an event conditional on a single parent event.

        Args:
            name: The name of the event.
            parent_event: The name of the parent event it depends on.
            prob_if_true: Probability if parent is true.
            prob_if_false: Probability if parent is false.

        Returns:
            The created Event object.
        """
        if name in self.events:
            raise ValueError(f"Event '{name}' already exists in the scenario.")
        if parent_event not in self.events:
            raise ValueError(f"Parent event '{parent_event}' must be added before '{name}'.")

        event = Event(name, 0.0) # Base probability is ignored for conditional events
        event.make_conditional(parent_event, prob_if_true, prob_if_false)
        self.events[name] = event
        self.event_order.append(name)
        return event

    def add_multi_conditional_event(self, name: str, parent_events: List[str],
                                    condition_probs: Dict[str, float]) -> Event:
        """
        Add an event conditional on multiple parent events.

        Args:
            name: The name of the event.
            parent_events: List of parent event names it depends on.
            condition_probs: Dictionary mapping states (e.g., "11") to probabilities.

        Returns:
            The created Event object.
        """
        if name in self.events:
            raise ValueError(f"Event '{name}' already exists in the scenario.")
        for parent in parent_events:
            if parent not in self.events:
                raise ValueError(f"Parent event '{parent}' must be added before '{name}'.")

        event = Event(name, 0.0)
        event.make_multi_conditional(parent_events, condition_probs)
        self.events[name] = event
        self.event_order.append(name)
        return event

    def get_event_index(self, name: str) -> int:
        """Get the index of an event in the scenario (used for quantum register mapping)."""
        if name not in self.event_order:
            raise ValueError(f"Event '{name}' not found.")
        return self.event_order.index(name)
