
import flask
from wsgiref.simple_server import make_server
app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route('/')
def hello_world():
    return 'Hello world'


with make_server('', 5000, app) as server:
    print("F")

server.serve_forever()
