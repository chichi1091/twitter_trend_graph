# -*- coding: utf-8 -*-
import json
import sys
import datetime, time
import re
from requests_oauthlib import OAuth1Session
from twitter_trend_graph import settings
from dashboards.models.tweets import Tweets

SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
SEARCH_KEYWORD = u'#lovelive'


def tweet_search_job():
    session = OAuth1Session(settings.TWITTER['CONSUMER_KEY'], settings.TWITTER['CONSUMER_SECRET']
                            , settings.TWITTER['ACCESS_TOKEN'], settings.TWITTER['ACCESS_TOKEN_SECRET'])

    yesterday = datetime.date.today() - datetime.timedelta(1)
    params = {'q': SEARCH_KEYWORD, 'count': 200, 'lang': 'ja', 'until': yesterday.strftime("%Y-%m-%d")}

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
            print("---{} sec sleep".format(sec))
            time.sleep(sec + 5)
            continue

        if response.status_code != 200:
            print("Twitter API Error: %d" % response.status_code)
            print("Twitter API Error: {}".format(response.text))
            sys.exit(1)

        limit = response.headers['X-Rate-Limit-Remaining']
        if limit == 0:
            sec = int(response.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.datetime.now().timetuple())
            time.sleep(sec + 5)
            continue

        error_count = 0

        res_text = json.loads(response.text)
        if len(res_text) == 0:
            break

        for tweet in res_text['statuses']:
            match = re.search(r'/(全員|ふぁぼ|ファボ|定期|相互)/', tweet['text'])
            if match is None:
                # print(tweet['text'])
                # print('----------')
                tweet = Tweets(text=tweet['text'], tweet_date=yesterday)
                tweet.save()

        params['max_id'] = tweet['id'] - 1

