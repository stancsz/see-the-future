import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from see_the_future.core import Scenario

class ResultAnalyzer:
    """Analyzes and visualizes the results of a scenario simulation."""
    def __init__(self, scenario: Scenario, counts: Dict[str, int]):
        """
        Initialize the ResultAnalyzer.

        Args:
            scenario: The Scenario object defining the events.
            counts: The measurement counts from the simulator.
        """
        self.scenario = scenario
        self.counts = counts
        self.total_shots = sum(counts.values())
        self.probabilities: Dict[str, float] = {}

        # In Qiskit, bit strings are returned in little-endian order (q_n, ..., q_0).
        # We need to reverse the bitstring to match the order of events we added.
        for state, count in counts.items():
            reversed_state = state[::-1]
            self.probabilities[reversed_state] = count / self.total_shots

    def get_most_likely_scenarios(self, top_n: int = 5) -> List[Tuple[str, float, Dict[str, bool]]]:
        """
        Get the most probable outcomes from the simulation.

        Args:
            top_n: Number of top scenarios to return.

        Returns:
            A list of tuples: (state_string, probability, dictionary_of_event_outcomes).
        """
        sorted_probs = sorted(self.probabilities.items(), key=lambda item: item[1], reverse=True)

        results = []
        for state, prob in sorted_probs[:top_n]:
            event_outcomes = {}
            for i, event_name in enumerate(self.scenario.event_order):
                # Using the reversed state so index 0 is the first event added
                event_outcomes[event_name] = state[i] == "1"
            results.append((state, prob, event_outcomes))

        return results

    def plot_probabilities(self, top_n: int = 10, filename: str = "scenario_probs.png"):
        """
        Generate a bar chart of the scenario probabilities.

        Args:
            top_n: Number of top scenarios to plot.
            filename: Output filename for the plot.
        """
        sorted_probs = sorted(self.probabilities.items(), key=lambda item: item[1], reverse=True)

        labels = []
        values = []

        for state, prob in sorted_probs[:top_n]:
            # Create a more readable label
            outcome_strs = []
            for i, event_name in enumerate(self.scenario.event_order):
                status = "T" if state[i] == "1" else "F"
                outcome_strs.append(f"{event_name[:3]}:{status}")

            labels.append(" | ".join(outcome_strs))
            values.append(prob)

        plt.figure(figsize=(12, 6))
        bars = plt.barh(labels, values, color='skyblue')
        plt.xlabel("Probability")
        plt.title(f"Top {top_n} Possible Futures: {self.scenario.name}")
        plt.gca().invert_yaxis()  # Highest probability at top

        # Add text labels on bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                     f'{width:.2%}', ha='left', va='center')

        plt.tight_layout()
        plt.savefig(filename)
        print(f"Plot saved to {filename}")

    def print_report(self):
        """Print a summary report of the simulation."""
        print(f"--- Simulation Report: {self.scenario.name} ---")
        print(f"Total simulated shots: {self.total_shots}")
        print("\nTop 5 Most Likely Scenarios:")

        top_scenarios = self.get_most_likely_scenarios()
        for i, (state, prob, outcomes) in enumerate(top_scenarios, 1):
            print(f"\n{i}. Probability: {prob:.2%}")
            for event_name, outcome in outcomes.items():
                print(f"   - {event_name}: {'Occurs' if outcome else 'Does Not Occur'}")
        print("---------------------------------------")
