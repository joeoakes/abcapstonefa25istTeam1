# Project: abcapstonefa25istTeam1
# Purpose Details: Shor's algorithm using classical computing
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Giovanni, Alex
# Date Developed: 10/23/2025
# Last Date Changed: 10/23/2025
# Revision: Commented out benchmarking code temporarily to fix infinite loop bug

import math
import random
import time

# Benchmarking input/starter code
# start_time = time.time()

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

        # benchmarking code which shows the total time it took the code to process
        # Code was causing occasional infinite loop, commented out for now
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print(f"Elapsed time: {elapsed_time:.4f} seconds")