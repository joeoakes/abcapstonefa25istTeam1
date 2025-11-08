# Project: abcapstonefa25istTeam1
# Purpose Details: Runs both classical shor's algorithm file and the qiskit one made by the team using the simple RSA generation to generate initial numbers then logging in testing logs
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Alex Hammond
# Date Developed: 10/23/2025
# Last Date Changed: 11/6/2025
# Revision: Implemented QiskitShorNoise for later use

#!pip install -U qiskit qiskit-aer-gpu-cu11 --quiet

from ClassicalShorAlgorithm import shors_algorithm
from SimpleRSAGeneration import generate_rsa_keys
from QiskitShorsAlgorithm import QiskitShor
from QiskitShorsNoise import QiskitShorNoise

DIVIDER = " | "
log_filename = "TestingLogs.txt"

# Generate RSA keys
p, q, n, phi, e, d = generate_rsa_keys()


# Take message from user
message = input("Enter the message to encrypt: ")
qubits = input("Enter amount of working Qubits (default 6): ")
retries = input("Enter number of retries (default 10): ")

qubits = int(qubits) if qubits.strip() else 6
retries = int(retries) if retries.strip() else 10

# Encrypt message
encrypted_message = [pow(ord(ch), e, n) for ch in message]

# Run shor's algorithm with classical computing
shor_results = shors_algorithm(n)

# Display results

print("=== RSA Key Generation ===")
print(f"p = {p}, q = {q}, n = {n}")
print(f"e = {e}, d = {d}")
print(f"Encrypted message: {encrypted_message}\n")

print("=== Classical Shor's Algorithm Results ===")
print(f"n = {shor_results['n'] if 'n' in shor_results else n}")
print(f"a = {shor_results['a']}")
print(f"r = {shor_results['r']}")
print(f"Shor's possible factors: p = {shor_results['p']}, q = {shor_results['q']}")
print(f"Original RSA factors: p = {p}, q = {q}")


fp, fq, dm, r = QiskitShor(encrypted_message, n, e, qubits, retries)
print("=== Qiskit Shor's Algorithm Results ===")
print(f'n = {n}')
print(f'p = {fp}')
print(f'q = {fq}')
print(f'r = {r}')
print(f'decrypted message: {dm}')

# Log results to TestingLogs.txt
with open(log_filename, "a") as log_file:
    log_file.write(
        f"{message}{DIVIDER}"
        f"{encrypted_message}{DIVIDER}"
        f"({p},{q}){DIVIDER}"
        f"{n}{DIVIDER}"
        f"({shor_results['p']},{shor_results['q']}){DIVIDER}"
        f"{shor_results['r']}{DIVIDER}"
        f"{shor_results['a']}{DIVIDER}"
        f"({fp},{fq})\n"
    )