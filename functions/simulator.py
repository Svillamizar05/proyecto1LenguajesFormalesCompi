def simulate_dfa(dfa_data, input_string):
    validate_simulation_data(dfa_data, input_string)

    alphabet = dfa_data["alphabet"]
    initial_state = dfa_data["initialState"]
    accepting_states = set(dfa_data["acceptingStates"])
    transitions = dfa_data["transitions"]

    transition_map = build_dfa_transition_map(transitions)

    current_state = initial_state
    path = [current_state]

    for symbol in input_string:
        if symbol not in alphabet:
            raise ValueError(
                f"Symbol '{symbol}' does not belong to the DFA alphabet."
            )

        key = (current_state, symbol)

        if key not in transition_map:
            return {
                "path": path,
                "accepted": False
            }

        current_state = transition_map[key]
        path.append(current_state)

    return {
        "path": path,
        "accepted": current_state in accepting_states
    }


def validate_simulation_data(dfa_data, input_string):
    required_fields = [
        "dfaStates",
        "alphabet",
        "initialState",
        "acceptingStates",
        "transitions"
    ]

    for field in required_fields:
        if field not in dfa_data:
            raise ValueError(f"Missing required DFA field: {field}")

    if not isinstance(input_string, str):
        raise ValueError("The input string must be a string.")

    if dfa_data["initialState"] not in dfa_data["dfaStates"]:
        raise ValueError("The initial state must belong to dfaStates.")

    for accepting_state in dfa_data["acceptingStates"]:
        if accepting_state not in dfa_data["dfaStates"]:
            raise ValueError(
                f"Accepting state {accepting_state} does not belong to dfaStates."
            )


def build_dfa_transition_map(transitions):
    transition_map = {}

    for transition in transitions:
        origin = transition["from"]
        symbol = transition["symbol"]
        destination = transition["to"]

        key = (origin, symbol)

        if key in transition_map:
            raise ValueError(
                f"The DFA has more than one transition from "
                f"{origin} with symbol '{symbol}'."
            )

        transition_map[key] = destination

    return transition_map