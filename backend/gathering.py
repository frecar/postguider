import json
import re
from models import graph, Post, PostEncoder

max_searches = 50


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
        #if 'from' in element and 'category' in element['from']:
        #    continue

        post = Post(element)

        relevant_posts.append(post)

    data_for_graph = []
    for post in relevant_posts:
        data_for_graph.append([post.minutes_after_midnight, post.likes_count])

    print len(data_for_graph)

    with open("testdata.json", "wb") as file:
        file.write(json.dumps(data_for_graph))