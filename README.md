# See the Future

<img width="258" height="354" alt="logo" src="https://github.com/user-attachments/assets/8899e52d-b3dd-4ccb-90d1-d641d46e1bfe" />

**See the Future** is a Python-based framework that leverages the power of IBM Quantum Computing (via Qiskit) to perform advanced scenario simulations and predictive modeling.

By converting complex chains of conditional and independent probabilities into quantum circuits, the framework enables simulations of real-world "future" scenarios—ranging from market conditions and startup success to logistics and policy impact analysis.

## Features

- **Independent Events:** Define base events with a specific likelihood of occurrence.
- **Conditional Events:** Link events together, where the probability of a child event occurring is directly tied to the outcome of its parents.
- **Quantum Execution:** Simulates the scenario by mapping probabilities to $R_y$ and Controlled-$R_y$ gates on a Qiskit `QuantumCircuit`.
- **Hybrid Support:** Run locally via Qiskit's `AerSimulator` or seamlessly switch to real IBM Quantum Hardware using `qiskit-ibm-runtime`.
- **Visualization:** Generate clear, readable probability distribution graphs of all possible "future" states.

## Installation

1. Clone this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

You can find a complete, ready-to-run example in `main.py`.

### 1. Define your scenario
```python
from see_the_future.core import Scenario

# Create a scenario
scenario = Scenario("Market Simulation")

# Add independent events
scenario.add_independent_event("Strong Economy", 0.6)
scenario.add_independent_event("Competitor Action", 0.4)

# Add dependent event (Requires parent event outcome)
scenario.add_conditional_event("Secure Funding", "Strong Economy", 0.8, 0.3)
```

### 2. Build and run the simulation
```python
from see_the_future.engine import QuantumEngine
from see_the_future.simulator import ScenarioSimulator

engine = QuantumEngine(scenario)
circuit = engine.build_circuit()

# Run locally or set use_hardware=True for IBM Quantum
simulator = ScenarioSimulator(use_hardware=False)
counts = simulator.run(circuit, shots=10000)
```

### 3. Analyze the results
```python
from see_the_future.analyzer import ResultAnalyzer

analyzer = ResultAnalyzer(scenario, counts)
analyzer.print_report()
analyzer.plot_probabilities(filename="scenario_probs.png")
```

## Running on Real IBM Quantum Hardware

To execute your simulation on real quantum processors:

1. Create an IBM Quantum account.
2. Save your API token locally using the `qiskit-ibm-runtime` tool:
   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_IBM_TOKEN", set_as_default=True)
   ```
3. Set `use_hardware=True` when initializing the `ScenarioSimulator`.
