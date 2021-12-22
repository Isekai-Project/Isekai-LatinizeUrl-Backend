from flask import Flask
from flask_cors import CORS
import config
import api

app = Flask(__name__)
CORS(app)

app.register_blueprint(api.api_blue)


@app.route('/')
def index():
    return 'Isekai ApiBase!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
