def convert_nfa_to_dfa(nfa_data):
    validate_nfa_data(nfa_data)

    states = nfa_data["states"]
    alphabet = nfa_data["alphabet"]
    initial_state = nfa_data["initial"]
    accepting_states = set(nfa_data["accepting"])
    transitions = nfa_data["transitions"]

    transition_map = build_transition_map(transitions)

    initial_subset = frozenset([initial_state])

    pending_subsets = [initial_subset]
    discovered_subsets = {initial_subset}

    dfa_transitions = []
    dfa_accepting_states = []

    while pending_subsets:
        current_subset = pending_subsets.pop(0)

        if current_subset.intersection(accepting_states):
            dfa_accepting_states.append(format_subset(current_subset))

        for symbol in alphabet:
            destination_subset = move(
                current_subset,
                symbol,
                transition_map
            )

            if not destination_subset:
                continue

            frozen_destination = frozenset(destination_subset)

            dfa_transitions.append({
                "from": format_subset(current_subset),
                "symbol": symbol,
                "to": format_subset(frozen_destination)
            })

            if frozen_destination not in discovered_subsets:
                discovered_subsets.add(frozen_destination)
                pending_subsets.append(frozen_destination)

    dfa_states = [
        format_subset(subset)
        for subset in discovered_subsets
    ]

    dfa_states.sort()
    dfa_accepting_states.sort()

    return {
        "dfaStates": dfa_states,
        "alphabet": alphabet,
        "initialState": format_subset(initial_subset),
        "transitions": dfa_transitions,
        "acceptingStates": dfa_accepting_states
    }


def validate_nfa_data(nfa_data):
    required_fields = [
        "states",
        "alphabet",
        "initial",
        "accepting",
        "transitions"
    ]

    for field in required_fields:
        if field not in nfa_data:
            raise ValueError(f"Missing required field: {field}")

    states = nfa_data["states"]
    alphabet = nfa_data["alphabet"]
    initial_state = nfa_data["initial"]
    accepting_states = nfa_data["accepting"]
    transitions = nfa_data["transitions"]

    if not isinstance(states, list):
        raise ValueError("The states field must be a list.")

    if not isinstance(alphabet, list):
        raise ValueError("The alphabet field must be a list.")

    if not isinstance(accepting_states, list):
        raise ValueError("The accepting field must be a list.")

    if not isinstance(transitions, list):
        raise ValueError("The transitions field must be a list.")

    if initial_state not in states:
        raise ValueError("The initial state must belong to states.")

    for accepting_state in accepting_states:
        if accepting_state not in states:
            raise ValueError(
                f"Accepting state {accepting_state} does not belong to states."
            )

    required_transition_fields = ["from", "symbol", "to"]

    for transition in transitions:
        if not isinstance(transition, dict):
            raise ValueError("Every transition must be a JSON object.")

        for field in required_transition_fields:
            if field not in transition:
                raise ValueError(
                    f"Missing transition field: {field}"
                )

        origin = transition["from"]
        symbol = transition["symbol"]
        destination = transition["to"]

        if origin not in states:
            raise ValueError(
                f"Transition origin {origin} does not belong to states."
            )

        if destination not in states:
            raise ValueError(
                f"Transition destination {destination} does not belong to states."
            )

        if symbol not in alphabet:
            raise ValueError(
                f"Transition symbol '{symbol}' does not belong to the alphabet."
            )


def build_transition_map(transitions):
    transition_map = {}

    for transition in transitions:
        origin = transition["from"]
        symbol = transition["symbol"]
        destination = transition["to"]

        key = (origin, symbol)

        if key not in transition_map:
            transition_map[key] = set()

        transition_map[key].add(destination)

    return transition_map


def move(current_subset, symbol, transition_map):
    destination_subset = set()

    for state in current_subset:
        key = (state, symbol)

        if key in transition_map:
            destination_subset.update(transition_map[key])

    return destination_subset


def format_subset(subset):
    ordered_states = sorted(subset)
    return "".join(str(state) for state in ordered_states)