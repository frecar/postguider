import facebook
import datetime
import json

from json import JSONEncoder

import math
from settings import oath_key

graph = facebook.GraphAPI(oath_key)


class PostEncoder(JSONEncoder):
    def default(self, o):
        return {'id': o.id,
                'minutes_after_midnight': o.minutes_after_midnight,
                'likes_count': o.likes_count,
                'message': o.message}


class Post:
    def __init__(self, facebook_api_data):
        self.id = facebook_api_data['id']

        self.message = ""
        if 'message' in facebook_api_data:
            self.message = facebook_api_data['message']

        self.created_time = datetime.datetime.strptime(facebook_api_data['created_time'],
                                                       '%Y-%m-%dT%H:%M:%S+0000')

        self.likes_count = self._count_likes()
        self.minutes_after_midnight = self._minutes_after_midnight_posted()

    def _count_likes(self):
        return len(graph.get_connections(self.id, "likes", limit=3000)['data'])

    def _minutes_after_midnight_posted(self):
        diff = self.created_time - self.created_time.replace(hour=0, minute=0, second=0,
                                                             microsecond=0)
        return int(round(diff.total_seconds() / 60, 0))


class Word:

    def __init__(self, word):
        self.word = word
        self.count = 1
        self.likes = 0

    def calculate_score(self):
        #score = (self.likes / (math.log(self.likes + 1, 2) + 1)) / self.count

        score = self.likes / max(math.log(self.count, 2), 1)
        score = score / max(self.likes, 1)

        if self.is_stopword():
            score = score / (math.log(self.likes + 1, 2) + 1)

        return score

    def is_stopword(self):
        data = ""

        with open("stopwords_english.json", "r") as file:
            data += file.read()
        with open("stopwords_french.json", "r") as file:
            data += file.read()
        with open("stopwords_norwegian.json", "r") as file:
            data += file.read()

        return self.word in data
