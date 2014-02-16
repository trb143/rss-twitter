import hashlib
import datetime
import feedparser
from string import Template

from common import Config, YamlReader, str_date, TweetManager, google_shorten_url


class RSSFeedExtractor():

    def __init__(self, yaml_file):
        self.feed = YamlReader()
        self.feed.read_file(yaml_file)
        self.control = YamlReader()

    def processor(self):
        feed = feedparser.parse('http://web.trinitymethodist.org.uk/weekly_feed')
        run_time = str_date(datetime.datetime.now())
        tweet_manager = TweetManager(self.feed.data['feeds']['path'])
        for post in feed.entries:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(post.title)
            for link in soup.find_all('a'):
                print link.get_text()
            print post.link, google_shorten_url(post.link)
            values = dict(title=link.get_text(), link=google_shorten_url(post.link))
            tweet = Template(self.feed.data['alert']['text']).safe_substitute(values)
            m = hashlib.md5()
            m.update(tweet)
            evnt = {'timestamp': run_time, 'tweet': tweet, 'id': m.hexdigest(), 'updated': run_time,
                'processed': False}
            tweet_manager.append(evnt)
        tweet_manager.save()

run = RSSFeedExtractor('/home/tim/Projects/rss-twitter/weekly-rss.yaml')
run.processor()



