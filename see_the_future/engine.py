import math
from typing import Dict, List, Optional
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from see_the_future.core import Scenario, Event

class QuantumEngine:
    """Translates a Scenario into a QuantumCircuit."""
    def __init__(self, scenario: Scenario):
        """
        Initialize the QuantumEngine.

        Args:
            scenario: The Scenario object defining the events.
        """
        self.scenario = scenario
        self.num_qubits = len(scenario.events)
        self.qr = QuantumRegister(self.num_qubits, "events")
        self.cr = ClassicalRegister(self.num_qubits, "measurements")
        self.circuit = QuantumCircuit(self.qr, self.cr)

    def _probability_to_angle(self, probability: float) -> float:
        """Convert a probability [0.0, 1.0] to a rotation angle for the Ry gate."""
        # Ry(theta) |0> creates state cos(theta/2)|0> + sin(theta/2)|1>
        # Probability of measuring 1 is sin^2(theta/2)
        # Therefore, theta = 2 * arcsin(sqrt(probability))
        return 2 * math.asin(math.sqrt(probability))

    def _apply_independent_event(self, event: Event, index: int):
        """Apply the rotation for an independent event."""
        angle = self._probability_to_angle(event.probability)
        self.circuit.ry(angle, self.qr[index])

    def _apply_conditional_event(self, event: Event, index: int):
        """Apply controlled rotations for an event dependent on a single parent."""
        parent_name = event.parent_events[0]
        parent_idx = self.scenario.get_event_index(parent_name)

        # Prob if parent is False (0) -> X gate on parent, CRY, X gate on parent
        prob_false = event.conditions.get("0", 0.0)
        angle_false = self._probability_to_angle(prob_false)
        self.circuit.x(self.qr[parent_idx])
        self.circuit.cry(angle_false, self.qr[parent_idx], self.qr[index])
        self.circuit.x(self.qr[parent_idx])

        # Prob if parent is True (1) -> CRY
        prob_true = event.conditions.get("1", 0.0)
        angle_true = self._probability_to_angle(prob_true)
        self.circuit.cry(angle_true, self.qr[parent_idx], self.qr[index])

    def _apply_multi_conditional_event(self, event: Event, index: int):
        """Apply controlled rotations for an event dependent on multiple parents."""
        parent_indices = [self.scenario.get_event_index(p) for p in event.parent_events]
        num_parents = len(parent_indices)

        for state, prob in event.conditions.items():
            if len(state) != num_parents:
                raise ValueError(f"State string '{state}' length must match number of parents ({num_parents}).")

            angle = self._probability_to_angle(prob)

            # Apply X gates to flip 0s to 1s for the multi-controlled gate
            for i, bit in enumerate(state):
                if bit == "0":
                    self.circuit.x(self.qr[parent_indices[i]])

            # Apply multi-controlled Ry gate using standard custom unitary decomposition or mcry
            # Qiskit circuit.mcry is deprecated in newer versions, but we can build it.
            # Using the simplest approach with standard gates if available, else custom implementation.
            # Let's use mcry if available, otherwise fallback.

            # A simpler way in recent Qiskit is to use `append` with a controlled RyGate.
            from qiskit.circuit.library import RYGate
            cry_gate = RYGate(angle).control(num_parents)
            self.circuit.append(cry_gate, [self.qr[i] for i in parent_indices] + [self.qr[index]])

            # Uncompute X gates
            for i, bit in enumerate(state):
                if bit == "0":
                    self.circuit.x(self.qr[parent_indices[i]])

    def build_circuit(self) -> QuantumCircuit:
        """
        Builds and returns the QuantumCircuit for the scenario.
        """
        # We assume the order of events guarantees parents are added before children.
        for index, event_name in enumerate(self.scenario.event_order):
            event = self.scenario.events[event_name]

            if not event.is_conditional:
                self._apply_independent_event(event, index)
            elif len(event.parent_events) == 1:
                self._apply_conditional_event(event, index)
            else:
                self._apply_multi_conditional_event(event, index)

        # Add measurement
        self.circuit.measure(self.qr, self.cr)

        return self.circuit
