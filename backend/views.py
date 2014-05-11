import json
import threading
from flask import make_response
from aggregate import analyze_time
from app import app
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
        'hours_to_wait': 1,
        'total_score': 0,
        'time_score': 0,
        'text_score': 0,
        'hint': "Building index",
    }

    try:
        data = Newsfeed.filter_only_posts_by_people(token)

    except Exception, e:
        es = ElasticSearch('http://localhost:9200/')

        try:
            es.create_index(token.lower())
            Newsfeed.newsfeed(token, [], 0, None, 1)

            t = threading.Thread(target=Newsfeed.newsfeed, args=(token, [], 0, None, 1500))
            t.setDaemon(True)
            t.start()

        except Exception, e:
            print e.message

        return json_response(
            response
        )

    hours_to_wait, post_now_score, buckets, average = analyze_time(data)

    response['total_score'] = Post.rate_text(text, token)[0] * 0.5 + post_now_score * 0.5
    response['text_score'] = Post.rate_text(text, token)[0]
    response['time_score'] = post_now_score

    response['hours_to_wait'] = hours_to_wait
    if Post.rate_text(text, token)[0] < 0.5:
        response['hint'] = "Try to write a better text\n"

    if post_now_score < 0.5:
        response['hint'] = "You should wait for %s hours to post this\n" % hours_to_wait

    response['post_now'] = response['score'] > 0.5

    if response['post_now']:
        response['hint'] = "You're really good at this! Post this right away!"

    return json_response(
        response
    )


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
    app.run(debug=True, port=5001, host="0.0.0.0")
