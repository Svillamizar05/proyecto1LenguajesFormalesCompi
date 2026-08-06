from functions.subset_construction import convert_nfa_to_dfa
from functions.simulator import simulate_dfa


def convert_automaton(nfa_data):
    try:
        return convert_nfa_to_dfa(nfa_data)
    except ValueError:
        raise
    except Exception as error:
        raise RuntimeError(
            "An unexpected error occurred during conversion."
        ) from error


def simulate_automaton(dfa_data, input_string):
    try:
        return simulate_dfa(dfa_data, input_string)
    except ValueError:
        raise
    except Exception as error:
        raise RuntimeError(
            "An unexpected error occurred during simulation."
        ) from error