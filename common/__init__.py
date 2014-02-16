__author__ = 'tim'
import datetime
import requests
import json


def str_date(date_value):
    return date_value.strftime('%Y-%m-%dT%H:%M:%S')


def date_str(date_value):
    return datetime.datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%S')


def google_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    return json.loads(r.text)['id']

from .yamlreader import YamlReader
from .tweet_manager import TweetManager
from .config import Config

