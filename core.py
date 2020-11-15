
import flask
from wsgiref.simple_server import make_server
app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route("/api/v1/hello-world-<int:variant>", methods=["GET"])
def index(variant):
    """Endpoint return number of variant(must be int)"""
    return f"Hello world"


with make_server('', 5000, app) as server:
    print("F")

server.serve_forever()
