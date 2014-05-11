# coding=utf-8
import json
import re
from models import graph, Post, PostEncoder, Word
from stemming.porter2 import stem
import math

max_searches = 100


def newsfeed(data, searches_completed, until):
    print "searching %s %s %s " % (searches_completed, until, "me")

    if not until:
        feed = graph.get_connections("me", "home", limit=50)
    else:
        feed = graph.get_connections("me", "home", limit=50, until=until)

    data.extend(feed['data'])

    if searches_completed < max_searches:

        if 'paging' in feed and 'next' in feed['paging']:
            previous = feed['paging']['next']
            until = re.findall("until=(\d+)", previous)

            newsfeed(data, searches_completed + 1, until[0])

    return data


def get_newsfeed(user_id):
    relevant_posts = []

    for element in newsfeed([], 0, None):
        if 'from' in element and 'category' in element['from']:
            continue

        post = Post(element)

        relevant_posts.append(post)

    data_for_graph = []
    for post in relevant_posts:
        data_for_graph.append([post.minutes_after_midnight, post.likes_count])

    with open("newsfeed.json", "wb") as file:
        file.write(json.dumps(data_for_graph, cls=PostEncoder))


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


def create_word_index(user_id):
    word_list = []

    with open("newsfeed.json", "r") as file:
        data = json.loads(file.read())

    for post in data:
        for word in post['message'].split(" "):

            word = word.lower()
            word = filter(lambda c: c.isalpha(), word)
            word = stem(word)

            if word == "":
                continue

            word_registerd = False

            for word_object in word_list:
                if word == word_object.word:
                    word_object.count += 1
                    word_object.likes += post['likes_count']
                    word_registerd = True

            if not word_registerd:
                word_list.append(Word(word))

    import operator

    word_list.sort(key=operator.methodcaller("calculate_score"), reverse=True)

    #for word in word_list[0:50]:
    #    print word.word, word.likes, word.count, word.calculate_score()

    return word_list


def rate_post(text):
    score = 0

    words = set([])

    word_index = create_word_index("me")

    for word in text.split(" "):
        word = word.lower()
        word = filter(lambda c: c.isalpha(), word)
        word = stem(word)
        if word:
            words.add(word)

    for word in words:
        word_indexed = False

        for index_word in word_index:
            if word == index_word.word:
                score += index_word.calculate_score()
                word_indexed = True
                break

        if not word_indexed:
            score += 0.5

    return score / (len(words)), len(words), text


# print rate_post("Facebook Hackathon: improving Google search!")
#print rate_post("Takk for alle gratulasjoner igår!:D")
# print rate_post("Marte")
# print rate_post("MGP. Hasn't seen it.")
# print rate_post(
#    """Da er det straks klart for enda en fantastisk Eurovision Song Contest kveld! Som jeg gleeeeder meg til dette, like spent og i Eurovision-rus hvert år ! Heeeeeia Norge !!!!""")
#
# print rate_post("I sandefjord og drikker øl")
# print rate_post("Koser oss på fjellet")
# print rate_post("Hver gang russland får poeng i eurovision, så buer folk x)")
#

#print rate_post("hawaii day forward")

#dump_newsfeed("")
#create_word_index("me")