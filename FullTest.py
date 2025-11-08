# Project: abcapstonefa25istTeam1
# Purpose Details: Display all aspects of the code using the other py. file
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn, Alex, Giovanni
# Date Developed: 11/05/2025
# Last Date Changed: 11/607/2025
# Revision: 1.0

import time
from RSA_utils import generate_rsa_keys, encrypt_message, decrypt_message
from ClassicalShorAlgorithm import run_classical_shor
from QiskitShorsAlgorithm import run_qiskit_shor

def main():
    print("=== Starting FullTest ===")
    # Generate RSA keys
    e, d, n, p, q = generate_rsa_keys()

    message = input("Enter the message to encrypt: ").strip() or "hello"
    qubits = input("Enter number of working qubits (default 6): ").strip()
    retries = input("Enter number of retries (default 10): ").strip()
    qubits = int(qubits) if qubits.isdigit() else 6
    retries = int(retries) if retries.isdigit() else 10

    ciphertext = encrypt_message(message, e, n)
    print(f"Encrypted message: {ciphertext}")

    # Classical Shor Algorithm
    print("\n=== Running Classical Shor's Algorithm ===")
    classical_start = time.time()
    classical_results = run_classical_shor(n)
    classical_runtime = time.time() - classical_start

    # Qiskit Shor Algorithm
    print("\n=== Running Qiskit Shor's Algorithm ===")
    qiskit_start = time.time()
    qiskit_results = run_qiskit_shor(n)
    qiskit_runtime = time.time() - qiskit_start

    # Decrypt message using classical results (if factors valid)
    decrypted_message = decrypt_message(ciphertext, d, n)

    # Print Classical Results
    print("\n=== Classical Shor's Algorithm Results ===")
    if classical_results:
        print(f"n = {n}")
        print(f"a = {classical_results.get('a', '?')}")
        print(f"r = {classical_results.get('r', '?')}")
        print(f"Factors: p = {classical_results.get('p', '?')}, q = {classical_results.get('q', '?')}")
        print(f"Runtime: {classical_runtime:.4f} seconds")
    else:
        print("No factors found.")

    # Print Qiskit Results
    print("\n=== Qiskit Shor's Algorithm Results ===")
    if qiskit_results:
        print(f"n = {n}")
        print(f"Factors: p = {qiskit_results.get('p', '?')}, q = {qiskit_results.get('q', '?')}")
        print(f"r (period) = {qiskit_results.get('r', '?')}")
        print(f"Decrypted message = {decrypted_message}")
        print(f"Runtime: {qiskit_runtime:.4f} seconds")
        print(f"Platform: {qiskit_results.get('platform', 'Unknown')}")
    else:
        print("No quantum factors found.")

    # Summary
    print("\n=== Full Test Summary ===")
    print(f"{'Algorithm':<20} {'n':<6} {'r':<6} {'Factors':<15} {'Decrypted':<10} {'Runtime(s)':<12} {'Platform'}")
    print("-" * 92)

    # Safely extract data from both runs
    def safe(key, data):
        return data.get(key, "?") if data else "?"

    print(f"{'Classical Shor':<20} {n:<6} {safe('r', classical_results):<6} "
          f"{str((safe('p', classical_results), safe('q', classical_results))):<15} "
          f"{decrypted_message:<10} {classical_runtime:<12.4f} {'Classical Simulator'}")

    print(f"{'Qiskit Shor':<20} {n:<6} {safe('r', qiskit_results):<6} "
          f"{str((safe('p', qiskit_results), safe('q', qiskit_results))):<15} "
          f"{decrypted_message:<10} {qiskit_runtime:<12.4f} {safe('platform', qiskit_results)}")

if __name__ == "__main__":
    main()
