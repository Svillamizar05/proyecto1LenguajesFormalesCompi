# NFA to DFA Web Server

## Overview

This project implements a REST API that converts a Nondeterministic Finite Automaton (NFA) into an equivalent Deterministic Finite Automaton (DFA) using the Subset Construction Algorithm.

It also provides an endpoint to simulate strings over the generated DFA.

---

## Environment

### Operating System

- macOS 26.5.1

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

The conversion is performed using the **Subset Construction Algorithm**.

The algorithm starts with the initial state of the NFA represented as a subset.

For every subset and every symbol of the alphabet, it computes all reachable NFA states.

Each different subset becomes a new DFA state.

A DFA state is marked as accepting if its subset contains at least one accepting state of the original NFA.

The algorithm finishes when no new subsets are generated.

---

## Authors

- Santiago Villamizar
- Juan Sebastian