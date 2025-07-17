from qiskit import QuantumCircuit

def parse_qasm_file(qasm_path):
    with open(qasm_path, 'r') as f:
        qasm_str = f.read()
    qc = QuantumCircuit.from_qasm_str(qasm_str)
    gate_sequence = []
    for instruction in qc.data:
        op = instruction.operation
        qargs = instruction.qubits
        cargs = instruction.clbits
        qubit_indices = [qc.qubits.index(q) for q in qargs]
        clbit_indices = [qc.clbits.index(c) for c in cargs]
        gate_sequence.append({
            'name': op.name,
            'qubits': qubit_indices,
            'clbits': clbit_indices
        })
    num_qubits = qc.num_qubits
    return gate_sequence, num_qubits

if __name__ == "__main__":
    gate_sequence, num_qubits = parse_qasm_file('your_circuit.qasm')
    print(f"Num qubits: {num_qubits}")
    for g in gate_sequence:
        print(g)