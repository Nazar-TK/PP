import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/hello-world-<int:variant>", methods=["GET"])
def home(variant):
    """tut bude text"""
    return f"Hello world {variant}"


app.run()