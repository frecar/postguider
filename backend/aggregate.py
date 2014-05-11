import datetime


def should_user_post(data):
    buckets = [0] * 24
    post_count = [0] * 24

    for post in data:
        bucket = post[0] / 60
        post_count[bucket] += 1
        buckets[bucket] += post[1]

    average = sum(buckets) / sum(post_count)

    for bucket, likes in enumerate(buckets):
        buckets[bucket] = buckets[bucket] / (post_count[bucket] + 1)

    print buckets

    hour_now = datetime.datetime.now().hour

    post_now = False
    hours_to_wait = 0

    if buckets[hour_now] >= average:
        post_now = True

    else:
        rest_list = buckets + buckets

        i = hour_now

        while rest_list[i] < average:
            i += 1

        hours_to_wait = i - hour_now

        post_now = False

    return post_now, hours_to_wait

