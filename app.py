from flask import Flask, render_template
from controllers.automata_controller import automata_controller

app = Flask(__name__)

app.register_blueprint(automata_controller)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)