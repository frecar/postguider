# coding=utf-8

import json
import datetime
from models import Post, PostEncoder, Newsfeed, dump_newsfeed_to_elasticsearch
from pyelasticsearch import ElasticSearch


def dump_newsfeed(user_id):
    relevant_posts = []

    for element in newsfeed([], 0, None):
        if 'from' in element and 'category' in element['from']:
            continue

        post = Post(element)
        relevant_posts.append(post)

    with open("newsfeed.raw", "wb") as file:
        try:
            file.write(str(relevant_posts))
        except TypeError, e:
            print "error with raw dump"
            print e.message

    with open("newsfeed.json", "wb") as file:
        file.write(json.dumps(relevant_posts, cls=PostEncoder))




def dump_relevant_newsfeed_to_elasticsearch(token):
    es = ElasticSearch('http://localhost:9200/')

    relevant_posts = []

    for element in Newsfeed.newsfeed(token, [], 0, None):
        if 'from' in element and 'category' in element['from']:
            continue

        post = Post(element, token)
        relevant_posts.append(post.serialize())

    data = {'posts': relevant_posts}
    es.index(token.lower(), "post", data, id=1)


def create_nor_list():
    ord = """
        a
à
â
abord
afin
ah
a
z
zut

"""

    words = set([])
    for word in ord.split("\n"):
        word = word.lower()
        if word:
            words.add(word)

    with open("stopwords_french.json", "wb") as file:
        file.write(json.dumps(list(words)))


#create_nor_list()

token = "CAACEdEose0cBACH7Uu7D1MG4f5ODcGo7ZCfZAVfUTEewPVFk5IGIp7ZB42ObUhylUnBu4HL0OApuMKB6OKDmPaQc54acZCFa1i2pyYvsZBUZAH6WttuhiZCrDUZCp7IZBk6hofmDosmZCdhuFRS8XR6l0jkgPwiTPB1yTXLmm2Nba9bAmdj9UokfRknJFtOAWJgEZCdykTZBjML0hgZDZD"

#dump_newsfeed_to_elasticsearch(token)