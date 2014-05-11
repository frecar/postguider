import json
import threading
from flask import make_response
from aggregate import analyze_time
from app import app
from tools import dump_newsfeed_to_elasticsearch
from models import PostEncoder, Post, Newsfeed
from pyelasticsearch import ElasticSearch


def json_response(data, status=200):
    response = make_response(json.dumps(data, cls=PostEncoder), status)
    response.mimetype = 'application/json'
    return response


@app.route('/analyze_post/<token>/<text>', methods=['GET'])
def analyze_post(token, text):
    response = {
        'post_now': False,
        'hours_to_wait': 0,
        'score': 0,
        'hint': "",
    }

    try:
        data = Newsfeed.filter_only_posts_by_people(token)

        hours_to_wait, post_now_score, buckets, average = analyze_time(data)

        response['score'] = Post.rate_text(text, token)[0] * 0.5 + post_now_score * 0.5
        response['hours_to_wait'] = hours_to_wait

        if Post.rate_text(text, token)[0] < 0.5:
            response['hint'] = "Try to write a better text\n"

        if post_now_score < 0.5:
            response['hint'] = "You should wait for %s hours to post this\n" % hours_to_wait


        response['post_now'] = response['score'] > 0.5

        if response['post_now']:
            response['hint'] = "You're good at this! Post this right away!"

        return json_response(
            response
        )

    except Exception, e:
        t = threading.Thread(target=dump_newsfeed_to_elasticsearch, args=(token,))
        t.setDaemon(True)
        t.start()

        return json_response({"hint": "Building index"})


@app.route('/graph/<token>/', methods=['GET'])
def graph_data(token):

    data = Newsfeed.filter_only_posts_by_people(token)
    hours_to_wait, post_now_score, buckets, average= analyze_time(data)

    return json_response(
        {'plot': data,
         'buckets': buckets,
         'average': average}
    )

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
