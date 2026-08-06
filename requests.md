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

Expected response:

```json
{
  "message": "NFA to DFA Web Server is running"
}
```

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

## 6. Test Invalid NFA

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