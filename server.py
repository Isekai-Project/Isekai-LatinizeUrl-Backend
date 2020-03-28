from flask import Flask, request, Response
import config
import api

app = Flask(__name__)
app.register_blueprint(api.api_blue)

@app.route('/')
def index():
    return 'Isekai ApiBase!'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)