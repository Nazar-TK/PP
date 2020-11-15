import flask
from wsgiref.simple_server import make_server
app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route("/api/v1/hello-world-<int:variant>", methods=["GET"])
def number(variant):
    """variant should be integer"""
    return f"Hello world {variant}"
if __name__ == '__main__':
    with make_server('', 5000, app) as server:
        print("pahaje!")

        server.serve_forever()