from flask import Flask
from flask_cors import CORS
import config
import api

PREFIX = config.URL_PREFIX or "/"

app = Flask(__name__)
CORS(app)

app.register_blueprint(api.api_blue, url_prefix=PREFIX)


@app.route('/')
@app.route(PREFIX + "/")
def index():
    return 'Isekai ApiBase!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
