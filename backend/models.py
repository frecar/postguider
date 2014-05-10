import facebook
import datetime
from json import JSONEncoder

from settings import oath_key

graph = facebook.GraphAPI(oath_key)


class PostEncoder(JSONEncoder):
    def default(self, o):
        return {'id': o.id,
                'minutes_after_midnight': o.minutes_after_midnight,
                'likes_count': o.likes_count}


class Post:
    def _count_likes(self):
        return len(graph.get_connections(self.id, "likes", limit=3000)['data'])

    def _minutes_after_midnight_posted(self):
        diff = self.created_time - self.created_time.replace(hour=0, minute=0, second=0,
                                                             microsecond=0)
        return int(round(diff.total_seconds() / 60, 0))

    def __init__(self, facebook_api_data):
        self.id = facebook_api_data['id']

        self.created_time = datetime.datetime.strptime(facebook_api_data['created_time'],
                                                       '%Y-%m-%dT%H:%M:%S+0000')

        self.likes_count = self._count_likes()
        self.minutes_after_midnight = self._minutes_after_midnight_posted()
