import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route("/api/v1/hello-world-<int:variant>", methods=["GET"])
def number(variant):
    """tut bude text"""
    return f"Hello world {variant}"




if __name__ == '__main__':
    app.run()