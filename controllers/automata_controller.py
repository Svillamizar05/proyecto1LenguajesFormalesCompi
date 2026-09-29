from flask import Blueprint, jsonify, request
from gateway.automata_gateway import (
    convert_automaton,
    simulate_automaton,
    minimize_automaton
)

automata_controller = Blueprint("automata_controller", __name__)


@automata_controller.route("/convert", methods=["POST"])
def convert():
    try:
        nfa_data = request.get_json()

        if nfa_data is None:
            return jsonify({
                "error": "The request body must contain valid JSON."
            }), 400

        result = convert_automaton(nfa_data)

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 500


@automata_controller.route("/simulate", methods=["POST"])
def simulate():
    try:
        request_data = request.get_json()

        if request_data is None:
            return jsonify({
                "error": "The request body must contain valid JSON."
            }), 400

        if "dfa" not in request_data:
            return jsonify({
                "error": "Missing required field: dfa"
            }), 400

        if "input" not in request_data:
            return jsonify({
                "error": "Missing required field: input"
            }), 400

        result = simulate_automaton(
            request_data["dfa"],
            request_data["input"]
        )

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 500


@automata_controller.route("/minimize", methods=["POST"])
def minimize():
    try:
        dfa_data = request.get_json(silent=True)

        if dfa_data is None:
            return jsonify({
                "error": "The request body must contain valid JSON."
            }), 400

        result = minimize_automaton(dfa_data)

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 500
