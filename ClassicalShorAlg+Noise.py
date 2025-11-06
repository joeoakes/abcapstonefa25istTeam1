# Project: abcapstonefa25istTeam1
# Purpose Details: Shor's algorithm with added Noise
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Giovanni
# Date Developed: 11/06/2025
# Last Date Changed: 11/06/2025
# Revision:

import math
import random

def shors_algorithm(n, noise_level=0.05):
    """
    Factor n using a simplified version of Shor's algorithm
    with simulated quantum noise.
    Returns (p, q) of factors or nothing if error.
    noise_level = chance (0 to 1) that noise affects a computation.
    """

    def multiplicative_order(a, n):
        if math.gcd(a, n) != 1:
            raise ValueError("a and n need to be coprime")
        x = 1
        for r in range(1, n):
            x = (x * a) % n
            # Simulated noise: small chance the modulo result is off by 1
            if random.random() < noise_level:
                x = (x + random.choice([-1, 1])) % n
            if x == 1:
                return r
        return 0

    while True:
        # Pick a random a value under 100
        a = random.randint(2, 99)
        if math.gcd(a, n) != 1:
            continue

        r = multiplicative_order(a, n)
        if r % 2 != 0:
            continue

        # Compute potential factors
        p = math.gcd(pow(a, r // 2, n) - 1, n)
        q = math.gcd(pow(a, r // 2, n) + 1, n)

        # Simulated noise small chance we flip p and q or get random values
        if random.random() < noise_level:
            p, q = q, p  # swap them
        if random.random() < noise_level / 2:
            p = random.randint(2, n-1)
        if random.random() < noise_level / 2:
            q = random.randint(2, n-1)

        # Only accept nontrivial factors
        if 1 < p < n and 1 < q < n:
            return {"p": p, "q": q, "r": r, "a": a}

# Example test
result = shors_algorithm(15, noise_level=0.1)
print(result)
