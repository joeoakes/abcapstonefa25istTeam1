# Project: abcapstonefa25istTeam1
# Purpose Details: Simple RSA Encryption Generation
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Ali Almalky, Alex Hammond
# Date Developed: 10/23/2025
# Last Date Changed: 10/23/2025
# Revision: Reduced prime_limit to 40

import math
from sympy import primerange
import random

def generate_rsa_keys(prime_limit=50):
    primes = list(primerange(11, prime_limit+1))
    
    p = random.choice(primes)
    q = random.choice(primes)
    while q == p:
        q = random.choice(primes)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    possible_es = [x for x in range(2, phi) if math.gcd(x, phi) == 1]
    e = random.choice(possible_es)
    
    d = pow(e, -1, phi)
    
    return p, q, n, phi, e, d
