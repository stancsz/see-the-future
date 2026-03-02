from see_the_future.core import Scenario
from see_the_future.engine import QuantumEngine
from see_the_future.simulator import ScenarioSimulator
from see_the_future.analyzer import ResultAnalyzer

def main():
    print("Welcome to 'See the Future' - Advanced Simulation")
    print("=================================================")

    # 1. Define the Scenario
    print("Defining scenario 'Global Supply Chain Disruption'...")
    scenario = Scenario("Global Supply Chain Disruption")

    # Independent events
    scenario.add_independent_event("Pandemic Outbreak", 0.05)
    scenario.add_independent_event("Geopolitical Tension", 0.3)
    scenario.add_independent_event("Natural Disaster", 0.1)

    # Conditional events
    # Factory Closure depends on Pandemic Outbreak
    scenario.add_conditional_event("Factory Closure", "Pandemic Outbreak", 0.9, 0.1)

    # Shipping Route Blocked depends on Geopolitical Tension
    scenario.add_conditional_event("Shipping Route Blocked", "Geopolitical Tension", 0.6, 0.05)

    # Multi-conditional event
    # Material Shortage depends on Factory Closure, Shipping Route Blocked, and Natural Disaster
    material_shortage_probs = {
        "000": 0.01,
        "001": 0.2,
        "010": 0.4,
        "011": 0.6,
        "100": 0.5,
        "101": 0.7,
        "110": 0.8,
        "111": 0.95
    }
    scenario.add_multi_conditional_event(
        "Material Shortage",
        ["Factory Closure", "Shipping Route Blocked", "Natural Disaster"],
        material_shortage_probs
    )

    # 2. Build the Quantum Circuit
    print("Translating scenario to quantum circuit...")
    engine = QuantumEngine(scenario)
    circuit = engine.build_circuit()

    print("\nGenerated Quantum Circuit:")
    print(circuit.draw(output='text'))

    # 3. Simulate the Future
    print("\nExecuting scenario simulation...")
    simulator = ScenarioSimulator(use_hardware=False)
    counts = simulator.run(circuit, shots=100000)

    # 4. Analyze Results
    print("\nAnalyzing results...")
    analyzer = ResultAnalyzer(scenario, counts)
    analyzer.print_report()

    # Generate visualization
    analyzer.plot_probabilities(filename="supply_chain_probs.png")

if __name__ == "__main__":
    main()
