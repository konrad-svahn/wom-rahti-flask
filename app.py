from crypt import methods
import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    ret = { 
        'method': request.method,
        'msg': 'webhoks work', 
        'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR') 
    }

    return ret


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
