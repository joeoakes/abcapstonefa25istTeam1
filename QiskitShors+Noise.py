# Project: abcapstonefa25istTeam1
# Purpose Details: Demonstrate how fractional representation relates to quantum phases
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Giovanni D
# Date Developed: Nov 6, 2025
# Last Date Changed: November 6, 2025
# Revision:

import numpy as np
from math import gcd
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
from fractions import Fraction
from qiskit.circuit.library import UnitaryGate
from sympy import primerange

# Compute d using modular inverse a⋅x≡1 mod m
def modinv(a, m):
    for d in range(2, m):
        if (a * d) % m == 1:
            return d
    return None


def modularn(a, N, n_work):
    D = 1 << n_work

    root = np.zeros((D, D), dtype=complex)
    for y in range(N):
        root[(a * y) % N, y] = 1.0
    for y in range(N, D):
        root[y, y] = 1.0

    # Build controlled version
    CU = np.eye(2 * D, dtype=complex)
    CU[D:, D:] = root

    gate = UnitaryGate(CU)
    print(f"a={a}, N={N}")
    return gate


def decrypt_message(cipher, n, d):
    decrypted_message = ''.join(chr(pow(c, d, n)) for c in cipher)
    return decrypted_message


def create_basic_noise_model():
    """
    Creates a simple noise model with small depolarizing and errors.
    You can adjust the probabilities to make it more or less noisy.
    """
    noise_model = NoiseModel()

    # Depolarizing error: randomizes qubit with some probability
    dep_error = depolarizing_error(0.01, 1)  # 1% chance of random error on 1-qubit gates
    dep_cx_error = depolarizing_error(0.02, 2)  # 2% on 2-qubit gates

    # Thermal relaxation: simulates qubits decaying or losing information
    thermal_error = thermal_relaxation_error(50e-6, 70e-6, 0.01)  # basic relaxation model

    # Add to all gates
    noise_model.add_all_qubit_quantum_error(dep_error, ["u1", "u2", "u3"])
    noise_model.add_all_qubit_quantum_error(dep_cx_error, ["cx"])
    noise_model.add_all_qubit_quantum_error(thermal_error, ["u2", "u3"])

    return noise_model


def shors_qiskit(N, n_count, retries):
    if N % 2 == 0:
        return 2, None, None


    sim_check = AerSimulator()
    gpu_ok = "GPU" in sim_check.available_devices()
    if gpu_ok:
        print("GPU available; using GPU simulator")
    else:
        print("GPU not available; using CPU simulator")

    # Create the noise model
    noise_model = create_basic_noise_model()
    print("🌀 Quantum noise model active (simulating real hardware errors)")

    backend = AerSimulator(
        method="statevector",
        device="GPU" if gpu_ok else "CPU",
        cuStateVec_enable=True,
        noise_model=noise_model
    )

    candidatebase = list(primerange(3, 200))

    for i, a in enumerate(candidatebase):
        if i >= retries:
            break
        print(f"a: {a}")
        if gcd(a, N) != 1:
            return gcd(a, N), None, None

        r = find_period_quantum(a, N, backend, n_count)
        if r is None or r % 2 != 0:
            continue

        x = pow(a, r // 2, N)
        if x == N - 1 or x == 1:
            continue

        factor1 = gcd(x + 1, N)
        factor2 = gcd(x - 1, N)

        if factor1 != 1 and factor1 != N:
            if factor2 == 1 or factor2 == N:
                factor2 = N // factor1
            return factor1, factor2, r
        if factor2 != 1 and factor2 != N:
            if factor1 == 1 or factor1 == N:
                factor1 = N // factor2
            return factor1, factor2, r
    return None, None, None


def find_period_quantum(a, N, backend, ncount):
    n_count = ncount
    n_target = int(np.ceil(np.log2(N)))

    qc = QuantumCircuit(n_count + n_target, n_count)

    qc.h(range(n_count))
    qc.x(n_count + n_target - 1)

    for j in range(n_count):
        power = 2 ** j
        cu_gate = modularn(pow(a, power, N), N, n_target)
        qc.append(cu_gate, [j] + list(range(n_count, n_count + n_target)))

    qc.append(QFTGate(num_qubits=n_count).inverse(True), range(n_count))
    qc.measure(range(n_count), range(n_count))

    qc = transpile(qc, backend)
    job = backend.run(qc, shots=2048)
    counts = job.result().get_counts()

    for measured, count in sorted(counts.items(), key=lambda x: -x[1]):
        phase = int(measured, 2) / (2 ** n_count)
        if phase == 0:
            continue
        r = phase_to_r(phase, a, N)
        if r is not None:
            print(f"[Quantum Subroutine] phase={phase:.5f}, r={r}")
            return r

    print("[Quantum Subroutine] No valid period found")
    return None


def decrypt_attack(N, e, n_count, retries):
    factored_p, factored_q, r = shors_qiskit(N, n_count, retries=retries)

    if not factored_p:
        raise RuntimeError(
            "Shor did not return factors; try again or use a different simulator seed."
        )

    if not factored_q:
        factored_q = N // factored_p

    phi_factored = (factored_p - 1) * (factored_q - 1)
    d_factored = modinv(e, phi_factored)
    return factored_p, factored_q, d_factored, r


def show_fraction_from_phase(phase: float, max_denominator=1 << 20):
    frac = Fraction(phase).limit_denominator(max_denominator)
    return frac.denominator


def phase_to_r(phase, a, N, max_den=None):
    if phase == 0:
        return None
    if max_den is None:
        max_den = 2 * N
    den = show_fraction_from_phase(phase, max_denominator=max_den)
    k = 1
    while den * k <= max_den:
        r_candidate = den * k
        if pow(a, r_candidate, N) == 1:
            return r_candidate
        k += 1
    return None


def QiskitShor(c, n, e, n_count, retries):
    factored_p, factored_q, d_factored, r = decrypt_attack(n, e, n_count, retries)
    return factored_p, factored_q, decrypt_message(c, n, d_factored), r
