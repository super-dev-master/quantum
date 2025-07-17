from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit.from_qasm_file("your_circuit.qasm")
qc.save_statevector()  # <-- Required in Qiskit 1.x and later

sim = AerSimulator(method="statevector")
result = sim.run(qc).result()
statevector = result.get_statevector()

# Now you can do your peak search, e.g.
import numpy as np
probs = np.abs(statevector)**2
peak_index = np.argmax(probs)
peak_bitstring = format(peak_index, f'0{qc.num_qubits}b')
peak_prob = probs[peak_index]
print(f"Peak bitstring: {peak_bitstring}, probability: {peak_prob}")