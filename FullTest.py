# Project: abcapstonefa25istTeam1
# Purpose Details: Runs both classical shor's algorithm file and the qiskit one made by the team using the simple RSA generation to generate initial numbers then logging in testing logs
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Alex Hammond
# Date Developed: 10/23/2025
# Last Date Changed: 11/6/2025
# Revision: 1.4

#!pip install -U qiskit qiskit-aer-gpu-cu11 --quiet

from ClassicalShorAlgorithm import shors_algorithm
from SimpleRSAGeneration import generate_rsa_keys
from QiskitShorsAlgorithm import QiskitShor
from QiskitShorsNoise import QiskitShorNoise
import logging
import colorlog
import time
import csv
import os


def benchmark(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()

    elapsed = end_time - start_time
    return result, elapsed

# Logging colors
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'light_white',      # was red, changed to green
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'light_red'
}

# Custom colors
BOLD_WHITE = '\033[97;1m'
BOLD_GREEN = '\033[92;1m'
BOLD_YELLOW = '\033[93;1m'
BOLD_CYAN = '\033[96;1m'
RESET = '\033[0m'

# Logging setup
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] - %(message)s%(reset)s",
    datefmt="%H:%M:%S",
    log_colors=log_colors
)

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# prevent double logger printing
if not logger.hasHandlers():
    logger.addHandler(handler)
else:
    logger.handlers.clear()
    logger.addHandler(handler)

# Generate RSA keys
p, q, n, phi, e, d = generate_rsa_keys()

# Take message from user
while True:
    message = input("Enter the message to encrypt (25 characters maximum): ")
    if len(message) > 25:
        print(f"{BOLD_YELLOW}Maximum allowed is 25{RESET}")
    elif len(message) == 0:
        print(f"{BOLD_YELLOW}Please enter a message{RESET}")
    else:
        break

# Take qubit amount from user
while True:
    qubits = input("Enter amount of working Qubits (default 6, max 16): ")
    if not qubits.strip():
        qubits = 6
        break
    elif qubits.isdigit():
        qubits = int(qubits)
        if qubits > 16:
            print(f"{BOLD_YELLOW}Maximum allowed is 16.{RESET}")

        elif qubits < 4:
            print(f"{BOLD_YELLOW}Minimum allowed is 4.{RESET}")

        else:
            break
    else:
        print(f"{BOLD_YELLOW}Please enter a valid number.{RESET}")


# Take retry amount from user
while True:
    retries = input("Enter number of retries (default 10, max 15): ")
    if not retries.strip():
        retries = 10
        break
    elif retries.isdigit():
        retries = int(retries)
        if retries > 15:
            print(f"{BOLD_YELLOW}Maximum allowed is 15.{RESET}")

        elif retries < 1:
            print(f"{BOLD_YELLOW}Minimum allowed is 1.{RESET}")

        else:
            break
    else:
        print(f"{BOLD_YELLOW}Please enter a valid number.{RESET}")


# Encrypt message
encrypted_message = [pow(ord(ch), e, n) for ch in message]

# Run shor's algorithm with classical computing
shor_results = shors_algorithm(n)

# Display results
logger.info(f"{BOLD_YELLOW}=== RSA Key Generation ===")
logger.info(f"p = {p}, q = {q}, n = {n}")
logger.info(f"e = {e}, d = {d}")
logger.info(f"Encrypted message: {encrypted_message}\n")

logger.info(f"{BOLD_YELLOW}=== Classical Shor's Algorithm Results ===")
logger.info(f"n = {shor_results['n'] if 'n' in shor_results else n}")
logger.info(f"a = {shor_results['a']}")
logger.info(f"r = {shor_results['r']}")
logger.info(f"Shor's possible factors: p = {shor_results['p']}, q = {shor_results['q']}")
logger.info(f"Original RSA factors: p = {p}, q = {q}")


(result, elapsed) = benchmark(QiskitShor, encrypted_message, n, e, qubits, retries)
fp, fq, dm, r, device_used = result
logger.info(f"{BOLD_YELLOW}=== Qiskit Shor's Algorithm Results ===")
logger.info(f'n = {n}')
logger.info(f'p = {fp}')
logger.info(f'q = {fq}')
logger.info(f'r = {r}')
logger.info(f'decrypted message: {dm}')
logger.info(f'{BOLD_CYAN} Qiskit Execution time: {elapsed} seconds')

# Base logging directory
base_log_dir = "LoggingResults"

# Select subfolder based on device used
if device_used.upper() == "GPU":
    log_dir = os.path.join(base_log_dir, "GPUResults")
else:
    log_dir = os.path.join(base_log_dir, "CPUResults")

# Make sure the directory exists
os.makedirs(log_dir, exist_ok=True)

# Create a timestamped CSV file in the selected directory
csv_filename = os.path.join(log_dir, f"ShorResults_{time.strftime('%Y%m%d_%H%M%S')}.csv")

# Define headers
headers = [
    "Device Used",
    "Original Message",
    "Encrypted Message",
    "RSA Factors",
    "N Value",
    "Classical Shor Factors",
    "Classical Shor r",
    "Classical Shor a",
    "Qiskit Shor Factors",
    "Qiskit Shor r",
    "Qiskit Shor Execution Time (Seconds)",
]

# Write headers once
with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

# Append a run's results
with open(csv_filename, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        device_used,
        message,
        encrypted_message,
        f"({p},{q})",
        n,
        f"({shor_results['p']},{shor_results['q']})",
        shor_results['r'],
        shor_results['a'],
        f"({fp},{fq})",
        r,
        f"{elapsed:.6f}"
    ])

print(f"{BOLD_YELLOW}Results logged to {csv_filename}")