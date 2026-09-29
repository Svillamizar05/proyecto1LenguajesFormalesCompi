# API Test Examples

## 1. Start the Server

```bash
python3 app.py
```

The server will run at:

```
http://127.0.0.1:5000
```

---

## 2. Test the Home Endpoint

```bash
curl http://127.0.0.1:5000
```

Expected status: **HTTP 200** with an HTML page (`Content-Type: text/html`). Open http://127.0.0.1:5000/ in a browser to use the web demonstration interface.

---

## 3. Test NFA to DFA Conversion

```bash
curl -X POST http://127.0.0.1:5000/convert \
-H "Content-Type: application/json" \
-d '{
  "states": [0,1,2,3],
  "alphabet": ["a","b"],
  "initial": 0,
  "accepting": [3],
  "transitions": [
    {
      "from": 0,
      "symbol": "a",
      "to": 1
    },
    {
      "from": 0,
      "symbol": "a",
      "to": 2
    },
    {
      "from": 1,
      "symbol": "b",
      "to": 3
    },
    {
      "from": 2,
      "symbol": "b",
      "to": 3
    }
  ]
}'
```

Expected response:

```json
{
  "dfaStates": [
    "0",
    "12",
    "3"
  ],
  "alphabet": [
    "a",
    "b"
  ],
  "initialState": "0",
  "transitions": [
    {
      "from": "0",
      "symbol": "a",
      "to": "12"
    },
    {
      "from": "12",
      "symbol": "b",
      "to": "3"
    }
  ],
  "acceptingStates": [
    "3"
  ]
}
```

---

## 4. Test DFA Simulation (Accepted String)

```bash
curl -X POST http://127.0.0.1:5000/simulate \
-H "Content-Type: application/json" \
-d '{
  "dfa": {
    "dfaStates": [
      "0",
      "12",
      "3"
    ],
    "alphabet": [
      "a",
      "b"
    ],
    "initialState": "0",
    "acceptingStates": [
      "3"
    ],
    "transitions": [
      {
        "from": "0",
        "symbol": "a",
        "to": "12"
      },
      {
        "from": "12",
        "symbol": "b",
        "to": "3"
      }
    ]
  },
  "input": "ab"
}'
```

Expected response:

```json
{
  "path": [
    "0",
    "12",
    "3"
  ],
  "accepted": true
}
```

---

## 5. Test DFA Simulation (Rejected String)

```bash
curl -X POST http://127.0.0.1:5000/simulate \
-H "Content-Type: application/json" \
-d '{
  "dfa": {
    "dfaStates": [
      "0",
      "12",
      "3"
    ],
    "alphabet": [
      "a",
      "b"
    ],
    "initialState": "0",
    "acceptingStates": [
      "3"
    ],
    "transitions": [
      {
        "from": "0",
        "symbol": "a",
        "to": "12"
      },
      {
        "from": "12",
        "symbol": "b",
        "to": "3"
      }
    ]
  },
  "input": "aa"
}'
```

Expected response:

```json
{
  "path": [
    "0",
    "12"
  ],
  "accepted": false
}
```

---

## 6. Test an NFA with Epsilon Transitions

The classic epsilon-NFA for the regular expression `(a|b)*abb`.

```bash
curl -X POST http://127.0.0.1:5000/convert \
-H "Content-Type: application/json" \
-d '{
  "states": [0,1,2,3,4,5,6,7,8,9,10],
  "alphabet": ["a","b"],
  "initial": 0,
  "accepting": [10],
  "transitions": [
    { "from": 0, "symbol": "",  "to": 1  },
    { "from": 0, "symbol": "",  "to": 7  },
    { "from": 1, "symbol": "",  "to": 2  },
    { "from": 1, "symbol": "",  "to": 4  },
    { "from": 2, "symbol": "a", "to": 3  },
    { "from": 3, "symbol": "",  "to": 6  },
    { "from": 4, "symbol": "b", "to": 5  },
    { "from": 5, "symbol": "",  "to": 6  },
    { "from": 6, "symbol": "",  "to": 1  },
    { "from": 6, "symbol": "",  "to": 7  },
    { "from": 7, "symbol": "a", "to": 8  },
    { "from": 8, "symbol": "b", "to": 9  },
    { "from": 9, "symbol": "b", "to": 10 }
  ]
}'
```

The five generated subsets are the ones produced by the algorithm in the
given book diagram:

```
01247     ->  A
1234678   ->  B
124567    ->  C
1245679   ->  D
12456710  ->  E   (accepting)
```

Feeding that DFA to `/simulate` accepts `abb`, `aabb` and `babb`, and rejects
`ab`, `abba` and the empty string.

---

## 7. Test Invalid NFA

```bash
curl -X POST http://127.0.0.1:5000/convert \
-H "Content-Type: application/json" \
-d '{
  "states": [0,1],
  "alphabet": ["a"],
  "initial": 0,
  "accepting": [1],
  "transitions": [
    {
      "from": 0,
      "symbol": "b",
      "to": 1
    }
  ]
}'
```

Expected response:

```json
{
  "error": "Transition symbol 'b' does not belong to the alphabet."
}
```

---

## 7. Find Equivalent DFA States (Assignment 2)

The official six-state DFA has initial state 0 and accepting states 1, 4, and 5. Send the DFA directly as the request body. The `-i` option displays the HTTP status and headers as well as the JSON body.

```bash
curl -i -X POST http://127.0.0.1:5000/minimize \
-H "Content-Type: application/json" \
-d '{
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
}'
```

Expected status: **HTTP 200**.

Expected response body:

```json
{
  "equivalentPairs": [
    [4, 5]
  ]
}
```

Only states 4 and 5 are equivalent. Both are accepting and both transition to state 5 on either symbol. The response lists equivalent pairs; it does not construct a minimized DFA.

---

## 8. Reject an Incomplete DFA (Assignment 2)

This DFA is missing the transition from state 1 with symbol `b`. Both states are reachable, but the transition function is incomplete.

```bash
curl -i -X POST http://127.0.0.1:5000/minimize \
-H "Content-Type: application/json" \
-d '{
  "dfaStates": [0, 1],
  "alphabet": ["a", "b"],
  "initialState": 0,
  "acceptingStates": [1],
  "transitions": [
    {"from": 0, "symbol": "a", "to": 1},
    {"from": 0, "symbol": "b", "to": 0},
    {"from": 1, "symbol": "a", "to": 1}
  ]
}'
```

Expected status: **HTTP 400**.

Expected response body:

```json
{
  "error": "Missing DFA transition from 1 with symbol 'b'. Every state must have exactly one transition per alphabet symbol."
}
```

`/minimize` requires exactly one transition per state and alphabet symbol and does not insert a sink state. Assignment 2 assumes that the supplied DFA has no unreachable states; the endpoint does not validate reachability.
