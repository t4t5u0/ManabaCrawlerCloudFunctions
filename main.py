import time

from flask import Request, Response, jsonify

import manaba


def post_get_tasks(request: Request) -> Response:

    userid: str
    password: str

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'userid' in request_json and 'password' in request_json:
        userid = request_json['userid']
        password = request_json['password']
    elif request_args and 'userid' in request_args and 'password' in request_args:
        userid = request_args['userid']
        password = request_args['password']

    # {"userid": userid, "password": password}
    time.sleep(0.5)
    return jsonify(manaba.get_tasks(userid, password))
