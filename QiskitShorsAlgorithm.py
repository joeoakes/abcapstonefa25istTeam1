# Project: abcapstonefa25istTeam1
# Purpose Details: Demonstrate how fractional representation relates to quantum phases
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn Brandt, Alex Hammond, Ali Almalky
# Date Developed: October 23, 2025
# Last Date Changed: November 2, 2025
# Revision: 1.2

# Import Needed Modules from Python's module
import numpy as np
from math import gcd
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
from fractions import Fraction
from qiskit.circuit.library import UnitaryGate
from sympy import primerange

# Compute d using the modular inverse a⋅x≡1 mod m
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

def shors_qiskit(N, n_count, retries):
    if N % 2 == 0:
        return 2, None, None

    # Try GPU; fall back to CPU if not available
    sim_check = AerSimulator() # Create an instance to check available devices
    gpu_ok = 'GPU' in sim_check.available_devices()
    if gpu_ok:
        print("GPU available; using GPU simulator")
    else:
        print("GPU not available; using CPU simulator")

    backend = AerSimulator(method="statevector",
                       device="GPU" if gpu_ok else "CPU",
                       cuStateVec_enable=True)

    candidatebase = list(primerange(3, 200))

    for i, a in enumerate(candidatebase):
        if i >= retries:
            break
        print(f"a: {a}")
        if gcd(a, N) != 1:
            return gcd(a, N), None, None

        # Quantum part
        r = find_period_quantum(a, N, backend, n_count)
        if r is None or r % 2 != 0:
            continue

        # Try to compute factors
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
    """
    Quantum subroutine for Shor's Algorithm:
    - Creates superposition in counting register
    - Performs modular exponentiation in superposition
    - Applies inverse QFT to estimate phase
    - Measures to determine the period 'r'
    """

    # Number of counting qubits (for precision)
    n_count = ncount

    # Number of target qubits (to represent N)
    n_target = int(np.ceil(np.log2(N)))

    # Build the quantum circuit
    qc = QuantumCircuit(n_count + n_target, n_count)

    # Step 1: Superposition on counting qubits
    qc.h(range(n_count))

    # Step 2: Initialize target register to |1⟩
    qc.x(n_count + n_target - 1)

    # Step 3: Controlled modular exponentiation
    # Each control qubit applies (a^(2^j) mod N)
    for j in range(n_count):
        power = 2 ** j
        cu_gate = modularn(pow(a, power, N), N, n_target)
        qc.append(cu_gate, [j] + list(range(n_count, n_count + n_target)))

    # Apply inverse Quantum Fourier Transform
    qc.append(QFTGate(num_qubits=n_count).inverse(True), range(n_count))

    # Step 5: Measure counting qubits
    qc.measure(range(n_count), range(n_count))

    # Step 6: Execute the circuit on simulator
    qc = transpile(qc, backend)
    job = backend.run(qc, shots=2048)
    counts = job.result().get_counts()

    # Step 7: Analyze results
    for measured, count in sorted(counts.items(), key=lambda x: -x[1]):
        phase = int(measured, 2) / (2 ** n_count)
        if phase == 0:
            continue  # try next most frequent bitstring
        r = phase_to_r(phase, a, N)
        if r is not None:
            print(f"[Quantum Subroutine] phase={phase:.5f}, r={r}")
            return r

    # If no valid r found
    print("[Quantum Subroutine] No valid period found")
    return None

def decrypt_attack(N, e,n_count,retries):
  factored_p, factored_q, r = shors_qiskit(N, n_count, retries=retries)

  if not factored_p:
      raise RuntimeError("Shor did not return factors; try running again (randomness) or use a different simulator seed.")

  if not factored_q:
    # Only one factor found; compute the other
    factored_q = N // factored_p

  phi_factored = (factored_p - 1) * (factored_q - 1)
  d_factored = modinv(e, phi_factored)
  return factored_p, factored_q, d_factored, r

def show_fraction_from_phase(phase: float, max_denominator:1<<20):
    # Convert the phase into a fraction
    frac = Fraction(phase).limit_denominator(max_denominator)
    return frac.denominator

def phase_to_r(phase, a, N, max_den=None):
    # phase is float in (0,1), returns candidate r or None
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
