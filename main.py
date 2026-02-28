from see_the_future.core import Scenario
from see_the_future.engine import QuantumEngine
from see_the_future.simulator import ScenarioSimulator
from see_the_future.analyzer import ResultAnalyzer

def main():
    print("Welcome to 'See the Future' - Quantum Scenario Simulation Framework")
    print("===================================================================")

    # 1. Define the Scenario
    print("Defining scenario 'Tech Startup Success'...")
    scenario = Scenario("Tech Startup Success")

    # Base independent events
    scenario.add_independent_event("Strong Economy", 0.6)
    scenario.add_independent_event("Competitor Action", 0.4)

    # Conditional events
    # If Economy is Strong (1), probability of securing funding is 0.8. Otherwise (0), 0.3.
    scenario.add_conditional_event("Secure Funding", "Strong Economy", 0.8, 0.3)

    # Multi-conditional event
    # Product Launch Success depends on both Secure Funding and Competitor Action
    # Format of states: "Funding Competitor"
    product_launch_probs = {
        "00": 0.2, # No funding, no competitor action -> 20% success
        "01": 0.05, # No funding, competitor acts -> 5% success
        "10": 0.9, # Funding, no competitor action -> 90% success
        "11": 0.5, # Funding, competitor acts -> 50% success
    }
    scenario.add_multi_conditional_event(
        "Product Launch Success",
        ["Secure Funding", "Competitor Action"],
        product_launch_probs
    )

    # 2. Build the Quantum Circuit
    print("Translating scenario to quantum circuit...")
    engine = QuantumEngine(scenario)
    circuit = engine.build_circuit()

    # Print the circuit representation
    print("\nGenerated Quantum Circuit:")
    print(circuit.draw(output='text'))

    # 3. Simulate the Future
    # Change use_hardware to True if you have configured Qiskit Runtime credentials locally
    print("\nExecuting scenario simulation...")
    simulator = ScenarioSimulator(use_hardware=False)
    counts = simulator.run(circuit, shots=10000)

    # 4. Analyze Results
    print("\nAnalyzing results...")
    analyzer = ResultAnalyzer(scenario, counts)
    analyzer.print_report()

    # Generate visualization
    analyzer.plot_probabilities(filename="startup_success_probs.png")

if __name__ == "__main__":
    main()
