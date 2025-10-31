from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.library import QFT
import numpy as np

def mod_exp_gate(a, N):

    qc = QuantumCircuit(1)
    phase = 2 * np.pi * (np.log(a) / np.log(N))  # Approximate phase
    qc.p(phase, 0)
    return qc.to_gate(label=f"U_mod({a},{N})")

def phase_estimation_U(U_gate, num_counting_qubits=4):

    total_qubits = num_counting_qubits + 1
    qc = QuantumCircuit(total_qubits, num_counting_qubits)

    # Put counting qubits in superposition
    for q in range(num_counting_qubits):
        qc.h(q)

    # Apply controlled powers of U
    for k in range(num_counting_qubits):
        power = 2 ** k
        qc.append(U_gate.power(power).control(), [k, num_counting_qubits])

    # Apply inverse QFT
    qc.append(QFT(num_counting_qubits, inverse=True), range(num_counting_qubits))

    # Measure counting qubits
    qc.measure(range(num_counting_qubits), range(num_counting_qubits))
    return qc

def run_phase_estimation(a, N, num_counting_qubits=4):

    print(f"\nRunning Quantum Phase Estimation for a={a}, N={N}...")

    U_gate = mod_exp_gate(a, N)
    qc = phase_estimation_U(U_gate, num_counting_qubits)

    # Use Aer's qasm simulator
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend=simulator, shots=1024).result()
    counts = result.get_counts(qc)

    print("Measurement results (binary counts):")
    for outcome, count in counts.items():
        print(f"{outcome}: {count}")

    return counts


if __name__ == "__main__":
    run_phase_estimation(a=7, N=15, num_counting_qubits=4)
