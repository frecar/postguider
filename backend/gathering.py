import facebook

from settings import oath_key
from models import Post


graph = facebook.GraphAPI(oath_key)

profile = graph.get_object("me")
feed = graph.get_connections("me", "home", limit=100)

for element in feed['data']:
    post = Post(element)

    print post.id, post.likes_count

