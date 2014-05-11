import json
from models import Post, PostEncoder


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


create_nor_list()