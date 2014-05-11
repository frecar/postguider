import json
from flask import make_response
from aggregate import analyze_time
from app import app
from models import PostEncoder, Post, Newsfeed


def json_response(data, status=200):
    response = make_response(json.dumps(data, cls=PostEncoder), status)
    response.mimetype = 'application/json'
    return response


@app.route('/analyze_post/<token>/<text>', methods=['GET', 'POST'])
def analyze_post(token, text):
    response = {
        'post_now': False,
        'hours_to_wait': 0,
        'score': 0,
        'hint': "",
    }

    data = Newsfeed.filter_only_posts_by_people(token)
    hours_to_wait, post_now_score = analyze_time(data)

    response['score'] = Post.rate_text(text)[0] * 0.5 + post_now_score * 0.5
    response['hours_to_wait'] = hours_to_wait

    if Post.rate_text(text)[0] < 0.5:
        response['hint'] = "Try to write a better text\n"

    if post_now_score < 0.5:
        response['hint'] = "You should wait for %s hours to post this\n" % hours_to_wait

    response['post_now'] = response['score'] > 0.5

    return json_response(
        response
    )


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")