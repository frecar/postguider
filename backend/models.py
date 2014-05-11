# coding=utf-8
import json
import re
from stemming.porter2 import stem

import facebook
import datetime
import math

from json import JSONEncoder

class PostEncoder(JSONEncoder):
    def default(self, o):
        return {'id': o.id,
                'minutes_after_midnight': o.minutes_after_midnight,
                'likes_count': o.likes_count,
                'message': o.message}


class Newsfeed:
    max_searches = 1

    @staticmethod
    def newsfeed(token, data, searches_completed, until):
        print "searching %s %s %s " % (searches_completed, until, "me")

        graph = facebook.GraphAPI(token)

        if not until:
            feed = graph.get_connections("me", "home", limit=50)
        else:
            feed = graph.get_connections("me", "home", limit=50, until=until)

        data.extend(feed['data'])

        if searches_completed < Newsfeed.max_searches:

            if 'paging' in feed and 'next' in feed['paging']:
                previous = feed['paging']['next']
                until = re.findall("until=(\d+)", previous)

                Newsfeed.newsfeed(token, data, searches_completed + 1, until[0])

        return data

    @staticmethod
    def filter_only_posts_by_people(token):
        relevant_posts = []

        for element in Newsfeed.newsfeed(token, [], 0, None):
            if 'from' in element and 'category' in element['from']:
                continue

            post = Post(element, token)

            relevant_posts.append(post)

        data_for_graph = []
        for post in relevant_posts:
            data_for_graph.append([post.minutes_after_midnight, post.likes_count])

        return data_for_graph

    @staticmethod
    def word_index():
        word_list = []

        with open("data/newsfeed.json", "r") as file:
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

        return word_list


class Post:
    def __init__(self, facebook_api_data, token):
        self.id = facebook_api_data['id']

        self.graph = facebook.GraphAPI(token)

        self.message = ""
        if 'message' in facebook_api_data:
            self.message = facebook_api_data['message']

        self.created_time = datetime.datetime.strptime(facebook_api_data['created_time'],
                                                       '%Y-%m-%dT%H:%M:%S+0000')

        self.likes_count = self._count_likes()
        self.minutes_after_midnight = self._minutes_after_midnight_posted()

    def _count_likes(self):
        return len(self.graph.get_connections(self.id, "likes", limit=3000)['data'])

    def _minutes_after_midnight_posted(self):
        diff = self.created_time - self.created_time.replace(hour=0, minute=0, second=0,
                                                             microsecond=0)
        return int(round(diff.total_seconds() / 60, 0))


    @staticmethod
    def rate_text(text):
        score = 0

        words = set([])

        word_index = Newsfeed.word_index()

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


class Word:
    def __init__(self, word):
        self.word = word
        self.count = 1
        self.likes = 0

    def calculate_score(self):
        #score = (self.likes / (math.log(self.likes + 1, 2) + 1)) / self.count

        score = self.likes / (math.log(self.count, 10) + 1)
        score = score / (self.likes + 1)

        if self.is_stopword():
            score = score / (math.log(self.likes + 1, 2) + 1)

        return score

    def is_stopword(self):
        data = ""

        with open("data/stopwords_english.json", "r") as file:
            data += file.read()
        with open("data/stopwords_french.json", "r") as file:
            data += file.read()
        with open("data/stopwords_norwegian.json", "r") as file:
            data += file.read()

        return self.word in data