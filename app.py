from flask import Flask
from controllers.automata_controller import automata_controller

app = Flask(__name__)

app.register_blueprint(automata_controller)


@app.route("/", methods=["GET"])
def home():
    return {
        "message": "NFA to DFA Web Server is running"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)