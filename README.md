# Automata Web Server — Assignments 1 and 2

## Overview

This project implements a REST API that converts a Nondeterministic Finite Automaton (NFA) into an equivalent Deterministic Finite Automaton (DFA) using the Subset Construction Algorithm.

It also provides an endpoint to simulate strings over the generated DFA.

Assignment 2 extends this same server with `POST /minimize`, which returns equivalent pairs of DFA states using the marking algorithm from Kozen Lecture 14. It does not construct a minimized DFA.

## Student Information

Students:

- Santiago Villamizar
- Juan Sebastian Ramirez

Class number: 4368

---

## Environment

### Operating System

- macOS 26.5.1 and Arch Linux in Intel silicon

### Programming Language

- Python 3.9.6

### Framework

- Flask 3.1.3

### Development Tool

- Visual Studio Code (version not recorded in the original project)

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
    ├── simulator.py
    └── minimization.py
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

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

The Environment section preserves the documented versions. `requirements.txt` pins Flask to version 3.1.3. Check the active environment with `python3 --version` and `python3 -m pip show Flask`.

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

### Convert an NFA into a DFA (Assignment 1)

```
POST /convert
```

### Simulate a DFA (Assignment 1)

```
POST /simulate
```

---

## Assignment 1 Algorithm

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
For example:

```json
{ "from": 0, "symbol": "", "to": 1 }
```

The epsilon symbol does not need to be listed in the `alphabet` field.

Subsets that have no transition for a given symbol simply have no entry in the output `transitions` list. The dead state is therefore implicit: when `/simulate` finds no transition for the current state and symbol, it stops and rejects the string.

---

## Assignment 2: Equivalent DFA States

### POST /minimize

Send the DFA directly as the JSON request body, with `Content-Type: application/json`. Do not wrap it in a `dfa` property (that wrapper is used by `/simulate`).

The endpoint expects a complete, deterministic DFA: every state must have exactly one transition for each alphabet symbol. Missing or duplicate transitions are rejected; no sink state is added automatically. Assignment 2 assumes that all input states are reachable from the initial state. The implementation does not check reachability or remove unreachable states.

All five fields below are required:

| Field | Meaning |
| --- | --- |
| `dfaStates` | List of distinct state identifiers; use consistently typed identifiers that can be sorted, such as integers or strings. |
| `alphabet` | List of distinct input symbols. |
| `initialState` | Initial state, belonging to `dfaStates`. |
| `acceptingStates` | List of accepting states, all belonging to `dfaStates`. |
| `transitions` | List of objects with `from`, `symbol`, and `to`; endpoints must belong to `dfaStates` and symbols to `alphabet`. |

Exact request example (the official six-state DFA):

```json
{
  "dfaStates": [0, 1, 2, 3, 4, 5],
  "alphabet": ["a", "b"],
  "initialState": 0,
  "acceptingStates": [1, 4, 5],
  "transitions": [
    {"from": 0, "symbol": "a", "to": 1},
    {"from": 0, "symbol": "b", "to": 2},
    {"from": 1, "symbol": "a", "to": 3},
    {"from": 1, "symbol": "b", "to": 4},
    {"from": 2, "symbol": "a", "to": 4},
    {"from": 2, "symbol": "b", "to": 3},
    {"from": 3, "symbol": "a", "to": 5},
    {"from": 3, "symbol": "b", "to": 5},
    {"from": 4, "symbol": "a", "to": 5},
    {"from": 4, "symbol": "b", "to": 5},
    {"from": 5, "symbol": "a", "to": 5},
    {"from": 5, "symbol": "b", "to": 5}
  ]
}
```

Successful response: **HTTP 200**.

```json
{
  "equivalentPairs": [
    [4, 5]
  ]
}
```

Each unordered pair is returned once as a two-element array, with its smaller state first. The list is in lexicographic order using the state identifiers' natural ordering (numeric for integers and lexical for strings). If no distinct states are equivalent, the response is `{"equivalentPairs": []}`.

Validation failures return **HTTP 400** with `{"error": "..."}`. For example, removing the transition from state 5 with symbol `b` produces:

```json
{
  "error": "Missing DFA transition from 5 with symbol 'b'. Every state must have exactly one transition per alphabet symbol."
}
```

Unexpected errors follow the existing gateway pattern and return **HTTP 500** with an error message. See [requests.md](requests.md) for complete commands for all endpoints.

### Kozen Lecture 14 Algorithm

1. Generate all unordered pairs of distinct states `{p, q}`. Initially, every pair is unmarked.
2. Mark each pair in which exactly one state is accepting. These states already differ on the empty string.
3. For each unmarked pair and each alphabet symbol `a`, examine the destination pair `{δ(p, a), δ(q, a)}`.
4. If the destination pair is marked, mark the current pair too. When both destinations are the same state, they cannot form a marked pair of distinct states.
5. Repeat complete passes until a pass produces no new marks.
6. The pairs that remain unmarked are equivalent: no input string distinguishes their acceptance behavior. Return them in lexicographic order.

### Integration with Assignment 1

The existing architecture is preserved:

```text
HTTP Request
→ Controller: POST /minimize
→ Gateway: minimize_automaton(dfa_data)
→ Functions: minimize_dfa(dfa_data)
→ HTTP Response
```

- `controllers/automata_controller.py` reads the JSON body and returns the result or an HTTP error through the existing Blueprint.
- `gateway/automata_gateway.py` calls the new algorithm, propagates `ValueError`, and wraps unexpected exceptions in `RuntimeError`, matching the previous gateway functions.
- `functions/minimization.py` validates the DFA and performs the marking algorithm independently of Flask and HTTP.
- `app.py` already registers the Blueprint, so no additional application registration is needed.

The existing `/convert` and `/simulate` behavior is preserved. `/convert` can produce a partial DFA because it omits transitions to the empty subset; such a result is not automatically a valid input to `/minimize`, which requires complete transitions. The new endpoint returns only equivalent pairs, not a minimized automaton.

---

## Web Demonstration Interface

After starting the server with `python3 app.py`, open http://127.0.0.1:5000/ in a browser. `GET /` serves the demonstration interface, replacing the previous home JSON message.

The interface uses HTML, CSS, and vanilla JavaScript, with three panels: NFA → DFA, Simulate DFA, and Minimize DFA. It sends requests to the same `/convert`, `/simulate`, and `/minimize` REST endpoints. Algorithm logic remains in Functions, behind the existing Controller → Gateway → Functions architecture.

For the Assignment 2 demonstration, select **Minimize DFA**, click **Load Assignment 2 Example**, then **Find Equivalent States**. The equivalent pairs shown come from the server response. Lists use JSON arrays, and transition table cells use numbers or quoted string identifiers. Click **Update table** after changing the states or alphabet. Backend validation messages are displayed in the result panel.

UI files are `templates/index.html`, `static/style.css`, and `static/app.js`. The conversion result can also be loaded into the simulation panel with **Use in Simulation**.
