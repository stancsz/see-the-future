from see_the_future.core import Scenario
from see_the_future.engine import QuantumEngine
from see_the_future.simulator import ScenarioSimulator
from see_the_future.analyzer import ResultAnalyzer

def main():
    print("Welcome to 'See the Future' - Quantum Scenario Simulation Framework")
    print("===================================================================")

    # 1. Define the Scenario
    print("Defining scenario 'Global Logistics Disruption'...")
    scenario = Scenario("Global Logistics Disruption")

    # Base independent events
    scenario.add_independent_event("Severe Weather Event", 0.3)
    scenario.add_independent_event("Port Strike", 0.2)
    scenario.add_independent_event("Fuel Price Spike", 0.4)

    # Conditional events
    # If Severe Weather Event (1), probability of Shipping Delay is 0.8. Otherwise (0), 0.2.
    scenario.add_conditional_event("Shipping Delay", "Severe Weather Event", 0.8, 0.2)

    # If Port Strike (1), probability of Labor Shortage is 0.9. Otherwise (0), 0.1.
    scenario.add_conditional_event("Labor Shortage", "Port Strike", 0.9, 0.1)

    # Multi-conditional event
    # Supply Chain Collapse depends on Shipping Delay, Labor Shortage, and Fuel Price Spike
    # Format of states: "Shipping Labor Fuel"
    supply_chain_probs = {
        "000": 0.01, # None occur -> 1% collapse
        "001": 0.05, # Only Fuel Spike -> 5% collapse
        "010": 0.10, # Only Labor Shortage -> 10% collapse
        "011": 0.30, # Labor + Fuel -> 30% collapse
        "100": 0.15, # Only Shipping Delay -> 15% collapse
        "101": 0.40, # Shipping + Fuel -> 40% collapse
        "110": 0.50, # Shipping + Labor -> 50% collapse
        "111": 0.90, # All three -> 90% collapse
    }
    scenario.add_multi_conditional_event(
        "Supply Chain Collapse",
        ["Shipping Delay", "Labor Shortage", "Fuel Price Spike"],
        supply_chain_probs
    )

    # 2. Build the Quantum Circuit
    print("Translating scenario to quantum circuit...")
    engine = QuantumEngine(scenario)
    circuit = engine.build_circuit()

    # Print the circuit representation
    print("\nGenerated Quantum Circuit:")
    print(circuit.draw(output='text'))

    # 3. Simulate the Future
    print("\nExecuting scenario simulation...")
    simulator = ScenarioSimulator(use_hardware=False)
    counts = simulator.run(circuit, shots=20000)

    # 4. Analyze Results
    print("\nAnalyzing results...")
    analyzer = ResultAnalyzer(scenario, counts)
    analyzer.print_report()

    # Generate visualization
    analyzer.plot_probabilities(filename="logistics_disruption_probs.png")

if __name__ == "__main__":
    main()
