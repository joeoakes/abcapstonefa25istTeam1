# Project: abcapstonefa25istTeam1
# Purpose Details: Shor's algorithm using classical computing
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author:
# Date Developed:
# Last Date Changed:
# Revision:

import sympy
import math

def shors_algorithm(a, n):
    """
   factor n using a simplified version of Shor's algorithm
    Returns (p, q) of factors or nothing if error
    """
    def multiplicative_order(a, n):
        if math.gcd(a, n) != 1:
            raise ValueError("a and n need to be coprime")
        x = 1
        for r in range(1, n):
            x = (x * a) % n
            if x == 1:
                return r
        return 0

    # Step 1: Find the order r
    r = multiplicative_order(a, n)
    if r % 2 != 0:
        return None  # Cannot factor  r if odd

    # Step 2: Compute potential factors
    p = math.gcd(pow(a, r // 2, n) - 1, n)
    q = math.gcd(pow(a, r // 2, n) + 1, n)

    if p * q == n:
        return (p, q)
    else:
        return None  # failed to factor n


a = 2
n = 364807
factors = shors_algorithm(a, n)
print(f"Factors of {n}: {factors}")

