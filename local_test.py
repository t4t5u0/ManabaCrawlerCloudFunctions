from flask import Flask, request

from main import post_get_tasks


if __name__ == "__main__":
    app = Flask(__name__)

    # $ curl -X 'POST' \                                                    [toybox]
    #   'http://127.0.0.1:8000/?userid=userid&password=password' \
    #   -H 'accept: application/json' \
    #   -d ''

    @app.route('/', methods=['POST'])
    def index():
        return post_get_tasks(request)

    app.run('127.0.0.1', 8000, debug=True)