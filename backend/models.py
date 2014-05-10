import facebook


class Post:

    def _count_likes(post_id):
        return len(graph.get_connections(post_id, "likes", limit=1000)['data'])

    def __init__(self, facebook_api_data):
        self.id = facebook_api_data['id']
        self.created_time = facebook_api_data['created_time']
        self.likes_count = self._count_likes()

