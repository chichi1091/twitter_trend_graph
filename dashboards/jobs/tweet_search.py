# -*- coding: utf-8 -*-
import json
import sys
import datetime, time
import re
import os
from pyspark.shell import sc
from requests_oauthlib import OAuth1Session
from twitter_trend_graph import settings
from dashboards.models.trends import Trends

SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
LIMIT_STATUS = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
SEARCH_KEYWORD = u'#lovelive'


def tweet_search_job():
    session = OAuth1Session(settings.TWITTER['CONSUMER_KEY'], settings.TWITTER['CONSUMER_SECRET']
                            , settings.TWITTER['ACCESS_TOKEN'], settings.TWITTER['ACCESS_TOKEN_SECRET'])

    yesterday = datetime.date.today() - datetime.timedelta(1)
    params = {'q': SEARCH_KEYWORD, 'count': 200, 'lang': 'ja', 'until': yesterday.strftime("%Y-%m-%d")}

    if os.path.isfile('tweets.txt'):
        os.remove('tweets.txt')
    f = open('tweets.txt', 'w')

    try:
        error_count = 0
        while True:
            response = session.get(SEARCH_URL, params=params)

            if response.status_code == 503:
                if error_count > 5:
                    raise Exception("エラー上限に達したため終了します")

                error_count += 1
                time.sleep(30)
                continue

            if response.status_code == 429:
                sec = int(response.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.datetime.now().timetuple())
                print("{0}---{1} sec sleep".format(datetime.date.today(), sec))
                time.sleep(sec + 5)
                continue

            if response.status_code != 200:
                print("Twitter API Error: %d" % response.status_code)
                print("Twitter API Error: {}".format(response.text))
                sys.exit(1)

            reset = 0
            limit = response.headers.get('X-Rate-Limit-Remaining', None)
            if limit is None:
                limit, reset = getLimitStatus(session)

            if limit == 0:
                sec = int(response.headers.get('X-Rate-Limit-Reset', reset)) - time.mktime(datetime.datetime.now().timetuple())
                time.sleep(sec + 5)
                continue

            error_count = 0

            res_text = json.loads(response.text)
            if len(res_text) == 0:
                break

            max_id = ""
            for tweet in res_text['statuses']:
                match = re.search(r'(全員|ふぁぼ|ファボ|定期|相互|RT)', tweet['text'], re.MULTILINE)
                if match is None:
                    f.write(tweet['text'] + '\n')
                max_id = tweet['id']

            params['max_id'] = max_id

    finally:
        f.close()

    try:
        textfile = sc.textFile("tweets.txt")
        print(textfile.count())

        words = textfile.flatMap(lambda line: line.split())
        words_filter = words.filter(lambda x: SEARCH_KEYWORD not in x)
        words_filter = words_filter.filter(lambda x: "#" not in x)
        words_filter = words_filter.filter(lambda x: len(x) >= 2)

        words_tuple = words_filter.map(lambda word: (word, 1))
        words_count = words_tuple.reduceByKey(lambda a, b: a + b)
        words_count_sorted = words_count.sortBy(lambda t: t[1], False)
        print(words_count_sorted.collect()[:10])

        for ranking in words_count_sorted.collect()[:10]:
            trends = Trends(target_date=yesterday, word=ranking[0], count=ranking[1])
            trends.save()
    finally:
        os.remove('tweets.txt')


def getLimitStatus(session):
    limit_response = session.get(LIMIT_STATUS)
    if limit_response.status_code == 503:
        raise Exception(limit_response.text)

    if limit_response.status_code != 200:
        print("Twitter API Error: %d" % limit_response.status_code)
        print("Twitter API Error: {}".format(limit_response.text))
        sys.exit(1)

    limit_json = json.loads(limit_response.text)
    remaining = limit_json['resources']['search']['/search/tweets']['remaining']
    reset = limit_json['resources']['search']['/search/tweets']['reset']

    return int(remaining), int(reset)
