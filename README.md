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

WSL 

Google Colabs

## Project Overview
  This GitHub repository will consist of the Team's effort to create a Qiskit circuit for decryption of a simple form of RSA. With in it will contain the files we used to compare and test the functionality of our circuit along with logging the test results when we begin testing.

## Project Objectives
  The objective of this project is to utilize Qiskit and Shor's Algorithm in order to decrypt a simplified form of RSA, within this project we will also run various tests to verify that our code is working correctly. 

## Project Structure
- LegacyFiles Folder
  - QiskitShor'sAlgorithmEXAMPLE.py
  - QiskitShorsNoise.py
  - TestingLogs(OLD).txt
- LoggingResults/CPUResults
- ClassicalShorAlgorithm.py
- FullTest.py
- QiskitShorsAlgorithm.py
- README.md
- SimpleRSAGeneration.py

### File Explanations

**LegacyFiles Folder**
- A folder with QiskitShorsNoise.py, which is no longer functional

**LoggingResults/CPUResults Folder**
- A folder containing our the results of our test logging

**ClassicalShorAlgorithm.py**
- Simple Shor's Algorithm program to work with classical computing to be used to verify the Qiskit code

**FullTest.py**
- Acts as the main run file running the RSA generation code, classical shor's code, and Qiskit algorithm code then logging outputs in TestingLogs.txt

**QiskitShorsAlgorithm.py**
- The main file for the Qiskit circuit that the team will work on

**README.md**
- Overview of the project along with important information

**SimpleRSAGeneration.py**
- Meant to act as a way to easily test both the classical shor's algorithm and the one our team will create with Qiskit

## Setup Guide
Prerequisites: Important to note is that for this to be fully functional, you'll want to run this in a Linux environment as it uses GPU CU11 simulation import, which is only available on Linux. You also need to have a GPU that can support CUDA cores, and you need to have Python.

Create and Activate a Virtual Environment
- To do this, run the following command:

python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip setuptools wheel

Clone the Github repository 
- To do this, run the following command:

cd ~/projects

git clone https://github.com/joeoakes/abcapstonefa25istTeam1

cd abcapstonefa25istTeam1

Run the following command to install the required packages:

```python3 -m pip install qiskit qiskit-aer colorlog sympy```

Run the Project:
- To do this, run the following command:
python FullTest.py

## Results and Screen Captures

