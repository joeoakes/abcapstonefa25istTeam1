# Project: abcapstonefa25istTeam1
# Purpose Details: Shor's algorithm using Qiskit Simulator with runtime logging
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn & Team
# Date Developed: 11/07/2025
# Last Date Changed: 11/07/2025
# Revision: 1.0

# QiskitShorsAlgorithm.py
# Simulated Shor’s Algorithm (Qiskit 2.x compatible)
import math
import random
import time
import logging
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
logger = logging.getLogger("QiskitShorsAlgorithm")
logger.debug("Logger initialized for QiskitShorsAlgorithm")

def gcd(a, b):
    """Compute GCD."""
    while b:
        a, b = b, a % b
    return a

def run_qiskit_shor(n, num_counting_qubits=6, max_retries=5):
    """Simulated Shor’s Algorithm using Qiskit-style logic."""
    start_time = time.time()
    logger.info(f"Starting Qiskit Shor's algorithm for n={n}")

    # handle small or prime n
    if n <= 3 or all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1)):
        return {
            "n": n, "p": None, "q": None, "r": None,
            "runtime": 0, "platform": "Qiskit Simulator"
        }

    for _ in range(max_retries):
        a = random.randint(2, n - 2)
        if gcd(a, n) != 1:
            continue

        # Build simple order-finding circuit (not actual factoring)
        qc = QuantumCircuit(num_counting_qubits + 4, num_counting_qubits)
        qc.h(range(num_counting_qubits))
        qc.x(num_counting_qubits)
        qc.barrier()
        qc.append(QFT(num_counting_qubits, inverse=True), range(num_counting_qubits))

        simulator = AerSimulator()
        compiled = transpile(qc, simulator)
        _ = simulator.run(compiled).result()

        # Fake order-finding (simulate result)
        r = random.randint(2, n // 2)
        if r % 2 != 0:
            continue

        x = pow(a, r // 2, n)
        if x == n - 1 or x == 1:
            continue

        p = gcd(x - 1, n)
        q = gcd(x + 1, n)
        if p * q == n:
            runtime = time.time() - start_time
            logger.info(
                f"Qiskit Shor completed | n={n} | base={a} | r={r} | factors=({p},{q}) | runtime={runtime:.4f}s | platform=Qiskit Simulator"
            )
            return {
                "n": n,
                "a": a,
                "r": r,
                "p": p,
                "q": q,
                "runtime": runtime,
                "platform": "Qiskit Simulator",
            }

    runtime = time.time() - start_time
    logger.warning(f"Qiskit Shor failed to find factors for n={n}")
    return {
        "n": n,
        "a": a,
        "r": 1,
        "p": n,
        "q": 1,
        "runtime": runtime,
        "platform": "Qiskit Simulator",
    }
