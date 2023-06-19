import json

from flask import Flask, request, Response
from flask_cors import CORS

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://chat.openai.com"}})

_TODOS = {}


@app.route("/todos/<string:username>", methods=["POST"])
def add_todo(username):
    request_data = request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request_data["todo"])
    return Response(response='OK', status=200)


@app.route("/todos/<string:username>", methods=["GET"])
def get_todos(username):
    return Response(response=json.dumps(_TODOS.get(username, [])), status=200)


@app.route("/todos/<string:username>", methods=["DELETE"])
def delete_todo(username):
    request_data = request.get_json(force=True)
    todo_idx = request_data["todo_idx"]
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return Response(response='OK', status=200)


@app.route("/logo.png", methods=["GET"])
def plugin_logo():
    filename = 'logo.png'
    return send_file(filename, mimetype='image/png')


@app.route("/.well-known/ai-plugin.json", methods=["GET"])
def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json", 'rt+') as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        print('debug here ', text)
        return Response(text, mimetype="text/json")


@app.route("/openapi.yaml", methods=["GET"])
def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return Response(text, mimetype="text/yaml")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
