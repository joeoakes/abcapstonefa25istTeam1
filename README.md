# RSA Quantum Decryption - abcapstonefa25istTeam1

## Course Information
Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem

Institution: Penn State Abington 

Term: Fall 2025

## Team and Members
Team Members: Alex Hammond, Ali Almalky, Madisyn Brandt, Giovanni DiBacco

## Technologies Used
Python 3

Qiskit

## Project Overview
  This GitHub repository will consist of the Team's effort to create a Qiskit circuit for decryption of a simple form of RSA. With in it will contain the files we used to compare and test the functionality of our circuit along with logging the test results when we begin testing.

## Project Objectives
  The objective of this project is to utilize Qiskit and Shor's Algorithm in order to decrypt a simplified form of RSA, within this project we will also run various tests to verify that our code is working correctly. 

## Project Structure
- ClassicalShorAlgorithm.py
- FullTest.py
- QiskitShor'sAlgorithm.py
- QiskitShor'sAlgorithmEXAMPLE.py
- README.md
- SimpleRSAGeneration.py
- TestingLogs.txt

### File Explanations
**ClassicalShorAlgorithm.py**
- Simple Shor's Algorithm program to work with classical computing to be used to verify the Qiskit code

**FullTest.py**
- Acts as the main run file running the RSA generation code, classical shor's code, and Qiskit algorithm code then logging outputs in TestingLogs.txt

**QiskitShor'sAlgorithm.py**
- The main file for the Qiskit circuit that the team will work on

**QiskitShor'sAlgorithmEXAMPLE.py**
- A publically available hardcoded version of Shor's aglorithm with Qiskit to learn and expirement on

**README.md**
- Overview of the project along with important information

**SimpleRSAGeneration.py**
- Meant to act as a way to easily test both the classical shor's algorithm and the one our team will create with Qiskit

**TestingLogs.txt**
- Will store the values when testing classical and/ or our team's custom Qiskit circuit to compare and learn from

## Setup Guide
For setup ensure you run the following install to have the proper packages
```!pip install qiskit qiskit-aer matplotlib pylatexenc sympy```
