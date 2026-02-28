import json
import warnings
from typing import Dict, Any, Optional

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2

class ScenarioSimulator:
    """Simulates or runs the QuantumCircuit on IBM Quantum hardware."""
    def __init__(self, use_hardware: bool = False, backend_name: Optional[str] = None):
        """
        Initialize the simulator.

        Args:
            use_hardware: If True, uses the IBM Quantum Runtime service.
                          Requires IBM Quantum credentials to be saved.
            backend_name: The name of the specific IBM backend to use if use_hardware is True.
        """
        self.use_hardware = use_hardware
        self.backend_name = backend_name
        self.backend = None

        if self.use_hardware:
            try:
                self.service = QiskitRuntimeService()
                if self.backend_name:
                    self.backend = self.service.backend(self.backend_name)
                else:
                    # Select the least busy backend
                    self.backend = self.service.least_busy(simulator=False, operational=True)
                print(f"Initialized IBM Quantum backend: {self.backend.name}")
            except Exception as e:
                warnings.warn(f"Failed to initialize IBM Quantum Service. Falling back to local simulator. Error: {e}")
                self.use_hardware = False

        if not self.use_hardware:
            self.backend = AerSimulator()
            print("Initialized local Aer simulator.")

    def run(self, circuit: QuantumCircuit, shots: int = 10000) -> Dict[str, int]:
        """
        Execute the circuit and return the measurement counts.

        Args:
            circuit: The compiled QuantumCircuit to run.
            shots: The number of times to run the circuit.

        Returns:
            A dictionary mapping binary state strings to counts.
        """
        if self.use_hardware:
            # Run on actual hardware using Sampler V2
            transpiled_circuit = transpile(circuit, self.backend)

            with Session(backend=self.backend) as session:
                sampler = SamplerV2(mode=session)

                # Execute the circuit
                job = sampler.run([transpiled_circuit], shots=shots)
                print(f"Job submitted to {self.backend.name}. Job ID: {job.job_id()}")

                # Wait for results
                result = job.result()
                pub_result = result[0]

                # Retrieve counts from BitArray
                counts = pub_result.data.measurements.get_counts()
                return counts

        else:
            # Run on local Aer simulator
            transpiled_circuit = transpile(circuit, self.backend)

            # Use basic local execute
            job = self.backend.run(transpiled_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts(circuit)
            return dict(counts)
