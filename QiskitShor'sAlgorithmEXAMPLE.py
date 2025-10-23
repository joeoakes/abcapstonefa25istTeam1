# Project: abcapstonefa25istTeam1
# Purpose Details: Example of Shor's algorithm with Qiskit using hardcoded values
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn Brandt
# Date Developed: October 23, 2025
# Last Date Changed: October 23, 2025
# Revision: 1.0

# Install required packages for Qiskit and plotting.
# This line is commented out to make loading faster — only use it if these
# packages are not already installed.
#!pip install qiskit qiskit-aer matplotlib pylatexenc

import numpy as np
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from math import gcd
from fractions import Fraction


# Creates a quantum gate that multiplies by 'a' under modulus 15.
# This is a key part of Shor's algorithm used to find factors.
def c_amod15(a, power):

    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must be 2, 4, 7, 8, 11 or 13")

    U = QuantumCircuit(4)

    # These swaps and flips represent how qubits move and change
    # Represent multiplication under modulus 15
    for _iteration in range(power):
        if a in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [7, 8]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)  # Flip the qubit state (like switching 0 ↔ 1 (superposition))

    # Convert the circuit to a reusable gate and make it controllable
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U

# Creates the inverse Quantum Fourier Transform (QFT) for 'n' qubits.
# This is used at the end of Shor's algorithm to find a repeating pattern in
# the numbers created by the system.
def qft_dagger(n):

    qc = QuantumCircuit(n)

    # Swap qubits to reverse the order (needed step for QFT)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)

    # Apply controlled rotations and Hadamard gates
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)

    qc.name = "QFT†"
    return qc

# Runs Quantum Phase Estimation (QPE) for multiplication by 'a' for modulus
# 15. This circuit helps find the hidden repeating pattern (period) of the
# function
def qpe_amod15(a):

    N_COUNT = 8  # Number of qubits used for counting
    qc = QuantumCircuit(4 + N_COUNT, N_COUNT)

    # Step 1: Put the qubits into superposition (0s and 1s)
    for q in range(N_COUNT):
        qc.h(q)

    # Step 2: Set an auxiliary register to |1⟩ (the starting state)
    qc.x(N_COUNT)

    # Step 3: Apply controlled multiplication gates with increasing powers
    for q in range(N_COUNT):
        qc.append(c_amod15(a, 2 ** q), [q] + [i + N_COUNT for i in range(4)])

    # Step 4: Apply the inverse QFT to reveal the pattern
    qc.append(qft_dagger(N_COUNT), range(N_COUNT))

    # Step 5: Measure the counting qubits to get the result
    qc.measure(range(N_COUNT), range(N_COUNT))

    # Run the circuit using the Qiskit simulator
    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(transpile(qc, aer_sim), shots=1, memory=True)
    readings = job.result().get_memory()

    print("Register Reading: " + readings[0])
    phase = int(readings[0], 2) / (2 ** N_COUNT)
    print(f"Corresponding Phase: {phase}")
    return phase


# Starting values
a = 7   # The number we will test with
N = 15  # The number we want to factor

FACTOR_FOUND = False
ATTEMPT = 0

# Repeat the process until a factor is found
while not FACTOR_FOUND:
    ATTEMPT += 1
    print(f"\nATTEMPT {ATTEMPT}:")
    phase = qpe_amod15(a)

    # Convert the measured phase into a fraction to guess the repeating pattern
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    print(f"Result: r = {r}")

    if phase != 0:
        # Use greatest common divisor (GCD) to find possible factors
        guesses = [gcd(a ** (r // 2) - 1, N), gcd(a ** (r // 2) + 1, N)]
        print(f"Guessed Factors: {guesses[0]} and {guesses[1]}")

        for guess in guesses:
            # Check if the guessed number divides N evenly
            if guess not in [1, N] and (N % guess) == 0:
                print(f"The algorithm found that {guess} divides {N} evenly!")
                FACTOR_FOUND = True # Prints results if it is even
