# coding=utf-8

import json
import datetime
from models import Post, PostEncoder, Newsfeed
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


def search_posts_elasticsearch(token):
    es = ElasticSearch('http://localhost:9200/')

    #for result in es.search("_type:post", index=token.lower())['hits']['hits']:
    #    print result["_source"]

    print es.search("id:sdifhsdihf", index="caacedeose0cban4zbmltsbcyxgzbzfrvq7uiqksk1uxep0njzgza7jtxei59ekp1izcjbg9czbum5qm0ojjuekaa3vwnn8tnxezcplgyaa2esvpi1dzcycai6xyvfwbrzco8quwns9orejsbecktw738yglnevljlqeascfgdfc0xdrjc1s0n40uun4ypytklsjarzand9gtfazdzd")

def dump_one_and_one_post_elasticsearch(token):
    es = ElasticSearch('http://localhost:9200/')

    relevant_posts = []

    for element in Newsfeed.newsfeed(token, [], 0, None):
        if 'from' in element and 'category' in element['from']:
            continue

        post = Post(element, token)

        es.index(token.lower(), "post", post.serialize())



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

token = "CAACEdEose0cBAFV0mETZB14RdmVWRMgISrV1kLCeZBeyYylvseb7KEVLdxtHRyVEswxlaB7oYl3lW3NF8ZC6jHwrLOTb7pIzRCraqOPLSOtZBUUhUPRYYzvMrNG7X1biY4DzdwZBguWCGYIQ7iOsfhi8onOaSYdlmB5HzPJL0TIHoV80x0m4IKcheWVzjLhKwZASB3V22fUgZDZD"

#dump_one_and_one_post_elasticsearch(token)
#search_posts_elasticsearch(token)

Newsfeed.newsfeed(token, [], 0, None)

#dump_newsfeed_to_elasticsearch(token)