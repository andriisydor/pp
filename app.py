from wsgiref.simple_server import make_server
from config import app
from api import api

app.register_blueprint(api)

with make_server('', 5000, app) as server:
    server.serve_forever()

# curl -v -XGET http://localhost:5000/api/v1/hello-world-9
# http://localhost:5000/api/v1/hello-world-9
