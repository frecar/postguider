import json
from flask import make_response
from aggregate import should_user_post_now
from app import app
from gathering import rate_post
from models import PostEncoder


def json_response(data, status=200):
    response = make_response(json.dumps(data, cls=PostEncoder), status)
    response.mimetype = 'application/json'
    return response


@app.route('/post_now/<token>/<text>', methods=['GET', 'POST'])
def post_now(token, text):
    #if not form.validate_on_submit():
    #    return "Bad format, you need to make a proper POST request with access token and text"

    response = {
        'post_now': False,
        'hours_to_wait': 0,
        'score': 0,
        'hint': "",
    }

    with open("testdata.json", "r") as file:
        data = json.loads(file.read())

    post_now_based_on_time, hours_to_wait, bucket_score = should_user_post_now(data)

    rate_time = 1

    if not post_now_based_on_time:
        rate_time = bucket_score

    response['score'] = rate_post(text)[0] * 0.5 + rate_time * 0.5
    response['hours_to_wait'] = hours_to_wait

    if rate_post(text)[0] < 0.5:
        response['hint'] = "Try to write a better text\n"

    if rate_time < 0.5:
        response['hint'] = "You should wait for %s hours to post this\n" % hours_to_wait

    response['post_now'] = response['score'] > 0.5

    return json_response(
        response
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
