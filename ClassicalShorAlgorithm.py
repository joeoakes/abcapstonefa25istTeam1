# Project: abcapstonefa25istTeam1
# Purpose Details: Shor's algorithm using classical computing with runtime logging
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Giovanni, Alex
# Date Developed: 10/23/2025
# Last Date Changed: 11/06/2025
# Revision: Added runtime logging

import math
import random
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
logger = logging.getLogger("ClassicalShorAlgorithm")

def gcd(a, b):
    """Compute the greatest common divisor."""
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(n):
    """Basic check for small primes."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_period(a, n):
    """Find period r for a^r ≡ 1 (mod n)"""
    r = 1
    apow = a % n
    while apow != 1:
        apow = (apow * a) % n
        r += 1
        if r > n:
            return None
    return r

def run_classical_shor(n):
    """Run the classical part of Shor’s algorithm."""
    logger.info(f"Starting Shor's algorithm for n={n}")
    start_time = time.time()

    if is_prime(n):
        logger.info(f"{n} is prime; no factors.")
        return None

    for _ in range(10):  # limit retries
        a = random.randint(2, n - 2)
        g = gcd(a, n)
        if g > 1:
            return {"n": n, "a": a, "r": None, "p": g, "q": n // g}

        r = find_period(a, n)
        if not r or r % 2 != 0:
            continue

        x = pow(a, r // 2, n)
        if x == n - 1 or x == 1:
            continue

        p = gcd(x - 1, n)
        q = gcd(x + 1, n)

        if p * q == n:
            runtime = time.time() - start_time
            logger.info(f"Factors found for n={n}: p={p}, q={q}, a={a}, r={r}")
            logger.info(f"Classical Shor runtime: {runtime:.4f} seconds")
            return {"n": n, "a": a, "r": r, "p": p, "q": q}

    logger.warning(f"Failed to find factors for n={n}")
    return None
