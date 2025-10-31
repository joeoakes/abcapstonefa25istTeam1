# Project: abcapstonefa25istTeam1
# Purpose Details: Demonstrate how fractional representation relates to quantum phases
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn Brandt
# Date Developed: October 23, 2025
# Last Date Changed: October 31, 2025
# Revision: 1.1

# Import fraction from Python's module
# This allows us to convert decimal values
from fractions import Fraction

def show_fraction_from_phase(phase: float, max_denominator: int = 20):
    # Convert the phase into a fraction
    frac = Fraction(phase).limit_denominator(max_denominator)

    # Display the starter decimal value
    print(f"Phase (decimal): {phase}")

    # Display the fraction’s numerator and denominator
    print(f"Fraction form: {frac.numerator}/{frac.denominator}")

    # In Shor’s Algorithm, the denominator shows the potential period (r value)
    print(f"Possible period (denominator): {frac.denominator}\n")

    # Return the fraction object
    return frac

# Hardcoded demo values
if __name__ == "__main__":
    # These represent examples of decimal values
    # from a Quantum Phase Estimation (QPE) step in Shor’s algorithm
    test_phases = [0.25, 0.3333, 0.2, 0.125]

    # Loop through each phase and display its fraction
    for phase in test_phases:
        show_fraction_from_phase(phase)
