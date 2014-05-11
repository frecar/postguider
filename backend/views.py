import json
from flask import make_response
from aggregate import should_user_post
from app import app

from models import PostEncoder


def json_response(data, status=200):
    response = make_response(json.dumps(data, cls=PostEncoder), status)
    response.mimetype = 'application/json'
    return response


@app.route('/post_now')
def post_now():
    data = ""

    with open("testdata.json", "r") as file:
        data = json.loads(file.read())

    return json_response(
        should_user_post(data)
    )


@app.route('/like_graph_data')
def like_graph_data():
    # data = get_newsfeed("me")

    with open("testdata.json", "r") as file:
        data = json.loads(file.read())

    return json_response(
        data
    )


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
