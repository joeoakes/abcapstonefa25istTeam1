# Project: abcapstonefa25istTeam1
# Purpose Details: Shor's algorithm using classical computing
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Giovanni, Alex
# Date Developed: 10/23/2025
# Last Date Changed: 10/23/2025
# Revision: Added some small changes to catch and retry errors

import math
import random

def shors_algorithm(n):
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
    while True:
        # Pick a random a value under 100
        a = random.randint(2,99)
        if math.gcd(a, n) != 1:
            continue

        r = multiplicative_order(a, n)
        if r % 2 != 0:
            continue

        # Compute potential factors
        p = math.gcd(pow(a, r // 2, n) - 1, n)
        q = math.gcd(pow(a, r // 2, n) + 1, n)

        # Only accept nontrivial factors
        if 1 < p < n and 1 < q < n:
            return {"p": p, "q": q, "r": r, "a": a}