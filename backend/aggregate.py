import datetime


def calculate_bucket_score(bucket, average):
    if bucket == average:
        return 0.5

    elif bucket < average:
        diff = average - bucket
        return max(0, 0.5 - (diff / average))

    elif bucket > average:
        diff = bucket - average
        return min(1, 0.5 + (diff / average))


def analyze_time(data):
    buckets = [0] * 24
    post_count = [0] * 24

    for post in data:
        bucket = post[0] / 60
        post_count[bucket] += 1
        buckets[bucket] += post[1]

    average = sum(buckets) / (sum(post_count) + 1)

    for bucket, likes in enumerate(buckets):
        buckets[bucket] = buckets[bucket] / (post_count[bucket] + 1)

    hour_now = datetime.datetime.now().hour

    hours_to_wait = 0

    if buckets[hour_now] < average:
        rest_list = buckets + buckets

        i = hour_now

        while rest_list[i] < average:
            i += 1

        hours_to_wait = i - hour_now

    return hours_to_wait, calculate_bucket_score(buckets[hour_now], average)
