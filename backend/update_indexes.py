from models import Newsfeed
from pyelasticsearch import ElasticSearch

es = ElasticSearch('http://localhost:9200/')

indices = set([])

for post in es.search("_type:post")['hits']['hits']:
    indices.add(post["_source"]["token"])


for index in indices:
    Newsfeed.newsfeed(index, [], 0, None, 1500)