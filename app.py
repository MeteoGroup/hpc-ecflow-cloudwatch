from flask import Flask
#from werkzeug.wsgi import DispatcherMiddleware
#from prometheus_client import make_wsgi_app


# Create my app
app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


@app.route("/metrics")
def metrics():
    return "my_first_metric 3.14"


# if __name__ == '__main__':
#  app.run(host='0.0.0.0', port=8000)

# Add prometheus wsgi middleware to route /metrics requests
#app_dispatch = DispatcherMiddleware(app, {'/metrics': make_wsgi_app()})

