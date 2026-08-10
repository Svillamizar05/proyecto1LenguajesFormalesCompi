# NFA to DFA Web Server

## Overview

This project implements a REST API that converts a Nondeterministic Finite Automaton (NFA) into an equivalent Deterministic Finite Automaton (DFA) using the Subset Construction Algorithm.

It also provides an endpoint to simulate strings over the generated DFA.

---

## Environment

### Operating System

- macOS 26.5.1 and Arch Linux in Intel silicon

### Programming Language

- Python 3.9.6

### Framework

- Flask 3.1.3

### Development Tool

- Visual Studio Code

---

## Project Structure

```
app.py
│
├── controllers/
│   └── automata_controller.py
│
├── gateway/
│   └── automata_gateway.py
│
└── functions/
    ├── subset_construction.py
    └── simulator.py
```

- **Controller**
  - Receives HTTP requests.
  - Validates input.
  - Returns HTTP responses.

- **Gateway**
  - Coordinates the execution of the algorithms.
  - Handles exceptions.

- **Functions**
  - Implements the automata algorithms.
  - Contains no HTTP-related code.

---

## Installation

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Server

Execute:

```bash
python3 app.py
```

The server will start at:

```
http://127.0.0.1:5000
```

---

## Available Endpoints

### Convert an NFA into a DFA

```
POST /convert
```

### Simulate a DFA

```
POST /simulate
```

---

## Algorithm

Every DFA state is a subset of NFA states. Two operations build those subsets:

- **move(T, a)**: all NFA states reachable from any state of `T` by consuming the symbol `a`.
- **epsilon-closure(T)**: all NFA states reachable from any state of `T` by following epsilon transitions only, without consuming input.

The algorithm starts with `epsilon-closure({initial})` as the first DFA state.

For every pending subset `T` and every symbol `a` of the alphabet, it computes `epsilon-closure(move(T, a))`. If that subset is not empty and has not been seen before, it becomes a new DFA state and is added to the pending list.

A DFA state is marked as accepting if its subset contains at least one accepting state of the original NFA.

The algorithm finishes when no new subsets are generated.

Each DFA state is named by concatenating the NFA states of its subset, so the subset `{0, 1, 3, 7}` is written `0137`.

### Epsilon transitions

An epsilon transition is written by leaving the symbol empty, or by using `ε` or `"epsilon"`:
as an example: 

```json
{ "from": 0, "symbol": "", "to": 1 }
```

The epsilon symbol does not need to be listed in the `alphabet` field.

Subsets that have no transition for a given symbol simply have no entry in the output `transitions` list. The dead state is therefore implicit: when `/simulate` finds no transition for the current state and symbol, it stops and rejects the string.

---

## Authors

- Santiago Villamizar
- Juan Sebastian Ramirez