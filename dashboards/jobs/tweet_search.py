# -*- coding: utf-8 -*-
import json
import sys
import datetime, time
from requests_oauthlib import OAuth1Session
from twitter_trend_graph import settings

SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
SEARCH_KEYWORD = u'#lovelive'


def tweet_search_job():
    session = OAuth1Session(settings.TWITTER['CONSUMER_KEY'], settings.TWITTER['CONSUMER_SECRET']
                            , settings.TWITTER['ACCESS_TOKEN'], settings.TWITTER['ACCESS_TOKEN_SECRET'])

    yesterday = datetime.date.today() - datetime.timedelta(1)
    params = {'q': SEARCH_KEYWORD, 'count': 100, 'lang': 'ja', 'until': yesterday.strftime("%Y-%m-%d")}

    for i in [1, 2]:
        print("{}回目".format(i))
        response = session.get(SEARCH_URL, params=params)

        if response.status_code != 200:
            print("Twitter API Error: %d" % response.status_code)
            print("Twitter API Error: {}".format(response.text))
            sys.exit(1)

        print('アクセス可能回数 %s' % response.headers['X-Rate-Limit-Remaining'])
        print('リセット時間 %s' % response.headers['X-Rate-Limit-Reset'])
        sec = int(response.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.datetime.now().timetuple())
        print('リセット時間 （残り秒数に換算） %s' % sec)

        res_text = json.loads(response.text)
        for tweet in res_text['statuses']:
            print('-----')
            print(tweet['created_at'])
            print(tweet['text'])

        params['max_id'] = tweet['id'] - 1


if __name__ == '__main__':
    tweet_search_job()
