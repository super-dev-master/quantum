from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

# Load your circuit (QASM file)
qc = QuantumCircuit.from_qasm_file("your_circuit.qasm")
qc.save_statevector()  # Needed in Qiskit 1.x+

print("Saved StateVector")

# Set up AerSimulator for GPU
sim = AerSimulator(method="statevector", device="GPU")
result = sim.run(qc).result()
statevector = result.get_statevector()

print("Got StateVector")

# Peak search
probs = np.abs(statevector) ** 2
peak_index = np.argmax(probs)
peak_bitstring = format(peak_index, f'0{qc.num_qubits}b')
peak_prob = probs[peak_index]
print(f"Peak bitstring: {peak_bitstring}, probability: {peak_prob}")