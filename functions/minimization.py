from itertools import combinations


def minimize_dfa(dfa_data):
    transition_map = validate_dfa_data(dfa_data)

    states = sorted(dfa_data["dfaStates"])
    alphabet = dfa_data["alphabet"]
    accepting_states = set(dfa_data["acceptingStates"])
    pairs = list(combinations(states, 2))
    marked_pairs = set()

    for p, q in pairs:
        if (p in accepting_states) != (q in accepting_states):
            marked_pairs.add(frozenset([p, q]))

    changed = True
    while changed:
        changed = False

        for p, q in pairs:
            pair = frozenset([p, q])
            if pair in marked_pairs:
                continue

            for symbol in alphabet:
                destination_pair = frozenset([
                    transition_map[(p, symbol)],
                    transition_map[(q, symbol)]
                ])

                # Equal destinations form a singleton, never a marked pair.
                if destination_pair in marked_pairs:
                    marked_pairs.add(pair)
                    changed = True
                    break

    return {
        "equivalentPairs": [
            [p, q] for p, q in pairs
            if frozenset([p, q]) not in marked_pairs
        ]
    }


def validate_dfa_data(dfa_data):
    if not isinstance(dfa_data, dict):
        raise ValueError("The DFA must be a JSON object.")

    required_fields = [
        "dfaStates", "alphabet", "initialState",
        "acceptingStates", "transitions"
    ]
    for field in required_fields:
        if field not in dfa_data:
            raise ValueError(f"Missing required DFA field: {field}")

    for field in ["dfaStates", "alphabet", "acceptingStates", "transitions"]:
        if not isinstance(dfa_data[field], list):
            raise ValueError(f"The {field} field must be a list.")

    states = dfa_data["dfaStates"]
    alphabet = dfa_data["alphabet"]
    accepting_states = dfa_data["acceptingStates"]

    try:
        state_set = set(states)
        symbol_set = set(alphabet)
        sorted(states)
    except TypeError as error:
        raise ValueError(
            "DFA states must be sortable scalar values and alphabet symbols "
            "must be scalar values."
        ) from error

    if len(state_set) != len(states) or len(symbol_set) != len(alphabet):
        raise ValueError("DFA states and alphabet symbols must not be repeated.")

    if dfa_data["initialState"] not in states:
        raise ValueError("The initial state must belong to dfaStates.")

    for state in accepting_states:
        if state not in states:
            raise ValueError(
                f"Accepting state {state} does not belong to dfaStates."
            )

    transition_map = {}
    for transition in dfa_data["transitions"]:
        if not isinstance(transition, dict):
            raise ValueError("Every transition must be a JSON object.")

        for field in ["from", "symbol", "to"]:
            if field not in transition:
                raise ValueError(f"Missing transition field: {field}")

        origin = transition["from"]
        symbol = transition["symbol"]
        destination = transition["to"]

        if origin not in states:
            raise ValueError(
                f"Transition origin {origin} does not belong to dfaStates."
            )
        if destination not in states:
            raise ValueError(
                f"Transition destination {destination} does not belong to dfaStates."
            )
        if symbol not in alphabet:
            raise ValueError(
                f"Transition symbol '{symbol}' does not belong to the alphabet."
            )

        key = (origin, symbol)
        if key in transition_map:
            raise ValueError(
                f"The DFA has more than one transition from "
                f"{origin} with symbol '{symbol}'."
            )
        transition_map[key] = destination

    for state in states:
        for symbol in alphabet:
            if (state, symbol) not in transition_map:
                raise ValueError(
                    f"Missing DFA transition from {state} with symbol '{symbol}'. "
                    "Every state must have exactly one transition per alphabet symbol."
                )

    return transition_map
