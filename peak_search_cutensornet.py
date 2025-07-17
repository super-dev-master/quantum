from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Load your circuit (from QASM)
qc = QuantumCircuit.from_qasm_file("your_circuit.qasm")

# Transpile for simulator (optional, but often helps performance)
sim = AerSimulator(method='statevector', device='GPU')
qc = transpile(qc, sim)

# Simulate to get statevector
result = sim.run(qc).result()
statevector = result.get_statevector()

# Calculate probabilities for all bitstrings
probs = np.abs(statevector) ** 2
peak_index = np.argmax(probs)
peak_bitstring = format(peak_index, f'0{qc.num_qubits}b')
peak_prob = probs[peak_index]

print(f"Peak bitstring: {peak_bitstring}, probability: {peak_prob}")