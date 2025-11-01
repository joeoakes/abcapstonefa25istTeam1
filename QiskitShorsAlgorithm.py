# Project: abcapstonefa25istTeam1
# Purpose Details: Demonstrate how fractional representation relates to quantum phases
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn Brandt, Alex Hammond
# Date Developed: October 23, 2025
# Last Date Changed: November 1, 2025
# Revision: 1.2

# Import Needed Modules from Python's module
import numpy as np
import random
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
    return ''.join([chr(pow(c, d, n)) for c in cipher])

def shors_qiskit(N, retries=5):
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

    candidatebase = list(primerange(2, 200))

    for i, a in enumerate(candidatebase):
        if i >= retries:
            break
        print(f"a: {a}")
        if gcd(a, N) != 1:
            return gcd(a, N), None, None

        # Quantum part
        r = find_period_quantum(a, N, backend)
        if r is None or r % 2 != 0:
            continue

        # Try to compute factors
        x = pow(a, r // 2, N)
        if x == N - 1 or x == 1:
            continue

        factor1 = gcd(x + 1, N)
        factor2 = gcd(x - 1, N)

        if factor1 * factor2 == N:
            return factor1, factor2, r
    return None, None, None

def find_period_quantum(a, N, backend):
    # Number of counting qubits
    n_count = 4  # Will implement qubit input later -Alex
    n_target = int(np.ceil(np.log2(N)))

    qc = QuantumCircuit(n_count + n_target, n_count)

    qc.h(range(n_count))
    qc.x(n_count + n_target - 1)

    for j in range(n_count):
        power = 2 ** j
        cu_gate = modularn(pow(a, power, N), N, n_target)
        qc.append(cu_gate, [j] + list(range(n_count, n_count + n_target)))


    # Giovanni put only the line for QFTGate inverse code under this comment and before the next with qc.append()


    # Measure counting register
    qc.measure(range(n_count), range(n_count))

    qc = transpile(qc, backend)
    job = backend.run(qc, shots=1024)
    counts = job.result().get_counts()

    measured = max(counts, key=counts.get)
    phase = int(measured, 2) / (2 ** n_count)
    if phase == 0:
        return None

    r = phase_to_r(phase, N)
    return r

def is_prime(n):
    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))

def decrypt_attack(N, e, retries=5):
  factored_p, factored_q, r = shors_qiskit(N, retries=retries)

  if not factored_p:
      raise RuntimeError("Shor did not return factors; try running again (randomness) or use a different simulator seed.")

  if not factored_q:
    # Only one factor found; compute the other
    factored_q = N // factored_p

  phi_factored = (factored_p - 1) * (factored_q - 1)
  d_factored = modinv(e, phi_factored)
  return factored_p, factored_q, d_factored

def show_fraction_from_phase(phase: float, max_denominator:1<<20):
    # Convert the phase into a fraction
    frac = Fraction(phase).limit_denominator(max_denominator)

    # Display the starter decimal value
    # print(f"Phase (decimal): {phase}")

    # Display the fraction’s numerator and denominator
    # print(f"Fraction form: {frac.numerator}/{frac.denominator}")

    # In Shor’s Algorithm, the denominator shows the potential period (r value)
    # print(f"Possible period (denominator): {frac.denominator}\n")

    # Return the fraction object
    return frac.numerator, frac.denominator

def phase_to_r(phase, N, max_den=None):
    # phase is float in (0,1), returns candidate r or None
    if phase == 0:
        return None
    if max_den is None:
        max_den = 1 << (int(np.ceil(np.log2(N))) + 1)
    num, den = show_fraction_from_phase(phase, max_denominator=max_den)
    return den

def QiskitShor(c, n, e, retries=5):

  factored_p, factored_q, d_factored = decrypt_attack(n, e, retries=retries)
  return factored_p, factored_q, decrypt_message(c, n, d_factored)