import numpy as np
from cuquantum import cutensornet as cutn
from parse_qasm import parse_qasm_file

def build_tensor_network(gate_sequence, num_qubits):
    """
    Builds a tensor network for the given gate sequence using cuTensorNet.
    """
    # Initialize cuTensorNet's handle
    handle = cutn.create()

    # Describe the tensor network
    desc = cutn.create_network_descriptor(handle, num_qubits)

    # Add gates to the tensor network
    for gate in gate_sequence:
        name = gate["name"]
        qubits = gate["qubits"]
        params = gate.get("params", [])
        try:
            if name in ("h", "x", "y", "z", "s", "sdg", "t", "tdg", "cx", "cz", "swap"):
                cutn.add_gate(handle, desc, name, qubits)
            elif name == "rz":
                theta = params[0] if params else 0.0
                cutn.add_gate(handle, desc, "rz", qubits, [theta])
            elif name == "ry":
                theta = params[0] if params else 0.0
                cutn.add_gate(handle, desc, "ry", qubits, [theta])
            elif name == "u3":
                # Decompose u3(theta, phi, lam) = rz(phi) ry(theta) rz(lam)
                theta, phi, lam = params if len(params) == 3 else (0.0, 0.0, 0.0)
                cutn.add_gate(handle, desc, "rz", qubits, [phi])
                cutn.add_gate(handle, desc, "ry", qubits, [theta])
                cutn.add_gate(handle, desc, "rz", qubits, [lam])
        except Exception as e:
            print(f"Warning: Could not add gate {name} on {qubits} with params {params}: {e}")

    return handle, desc

def get_output_probability(handle, desc, bitstring):
    """
    Computes the probability of a given output bitstring using cuTensorNet.
    """
    # Contract the tensor network to get the amplitude
    amp = cutn.contract_amplitude(handle, desc, bitstring)
    return abs(amp) ** 2

def greedy_peak_search(handle, desc, num_qubits):
    """
    Performs a greedy search for the most probable bitstring.
    """
    candidate = [0] * num_qubits
    best_prob = get_output_probability(handle, desc, candidate)
    improved = True
    while improved:
        improved = False
        for i in range(num_qubits):
            candidate_new = candidate.copy()
            candidate_new[i] ^= 1
            prob = get_output_probability(handle, desc, candidate_new)
            if prob > best_prob:
                best_prob = prob
                candidate = candidate_new
                improved = True
    return candidate, best_prob

if __name__ == "__main__":
    gate_sequence, num_qubits = parse_qasm_file('your_circuit.qasm')

    # Build tensor network
    handle, desc = build_tensor_network(gate_sequence, num_qubits)

    # Search for the most probable output
    peaked_output, prob = greedy_peak_search(handle, desc, num_qubits)

    print(f"Most probable output bitstring: {peaked_output}, probability: {prob}")

    # Clean up cuTensorNet resources
    cutn.destroy_network_descriptor(desc)
    cutn.destroy(handle)