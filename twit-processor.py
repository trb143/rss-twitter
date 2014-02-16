import tweepy
import json
import datetime

from common import YamlReader, str_date, date_str


class TwitProcessor():

    def __init__(self, yaml_file):
        self.feed = YamlReader()
        self.feed.read_file(yaml_file)

    def processor(self):
        handle = open(self.feed.data['feeds']['path'])
        events = json.load(handle)
        handle.close()
        run_time = datetime.datetime.now()
        tweets = []
        for event in events:
            if date_str(event['timestamp']) < run_time and not event['processed']:
                self.tweet(event['tweet'])
                event['processed'] = True
            tweets.append(event)
        data = open(self.feed.data['feeds']['path'], 'w')
        data.write(json.dumps(tweets))
        data.close()

    def tweet(self, text):

        CONSUMER_KEY = self.feed.data['twitter']['consumer_key']
        CONSUMER_SECRET = self.feed.data['twitter']['consumer_secret']
        ACCESS_KEY = self.feed.data['twitter']['access_key']
        ACCESS_SECRET = self.feed.data['twitter']['access_secret']

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        print api.me().name
        api.update_status(text)


run = TwitProcessor('/home/tim/Projects/rss-twitter/twitter.yaml')
run.processor()

