# Project: abcapstonefa25istTeam1
# Purpose: Provides simple RSA key generation, encryption, and decryption for testing
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn
# Date Developed: 11/07/2025

import random
import math

def gcd(a, b):
    """Compute the greatest common divisor."""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Compute modular inverse using Extended Euclidean Algorithm."""
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % phi

def generate_rsa_keys():
    """Generate small RSA keys for demonstration purposes."""
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    p = random.choice(primes)
    q = random.choice([x for x in primes if x != p])
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 5
    while gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)

    print(f"Generated RSA keys | p={p} | q={q} | n={n} | e={e} | d={d}")
    return (e, d, n, p, q)

def encrypt_message(message, e, n):
    """Encrypt a message string into a list of integers."""
    return [pow(ord(char), e, n) for char in message]

def decrypt_message(ciphertext, d, n):
    """Decrypt a list of integers into the original string."""
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])
