import json
from aggregate import should_user_post
from gathering import get_newsfeed

#get_newsfeed("me")

data = ""

with open("testdata.json", "r") as file:
    data = json.loads(file.read())

should_user_post(data)