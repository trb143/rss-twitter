import gflags
import httplib2
import datetime
from string import Template

from common import Config, YamlReader, str_date, TweetManager

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


class GoogleFeedExtractor():

    def __init__(self, yaml_file):
        self.config = Config()
        self.feed = YamlReader()
        self.feed.read_file(yaml_file)
        self.control = YamlReader()
        self.control.read_file(self.feed.data['google']['auth'])

    def processor(self):

        FLAGS = gflags.FLAGS

        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        # The client_id and client_secret are copied from the API Access tab on
        # the Google APIs Console
        flow = OAuth2WebServerFlow(client_id=self.control.data['google']['client_id'],
                                   client_secret=self.control.data['google']['client_secret'],
                                   scope=self.control.data['google']['scope'],
                                   user_agent=self.control.data['google']['user_agent'])

        # To disable the local server feature, uncomment the following line:
        # FLAGS.auth_local_webserver = False

        # If the Credentials don't exist or are invalid, run through the native client
        # flow. The Storage object will ensure that if successful the good
        # Credentials will get written back to a file.
        storage = Storage('calendar.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = run(flow, storage)

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build a service object for interacting with the API. Visit
        # the Google APIs Console
        # to get a developerKey for your own application.
        service = build(serviceName='calendar',
                        version='v3',
                        http=http,
                        developerKey=self.control.data['google']['developer_key'])

        run_time = datetime.datetime.now()
        page_token = None
        tweet_manager = TweetManager(self.feed.data['feeds']['path'])
        while True:
            events = service.events().list(calendarId=self.feed.data['google']['feed'],
                                           pageToken=page_token).execute()
            for event in events['items']:
                #print event['id'], event['start']['dateTime'], event['summary']
                timestamp = datetime.datetime.strptime(event['start']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                gmt_offset = int(event['start']['dateTime'][20:22]) if event['start']['dateTime'][20:22] else 0
                #timestamp = timestamp - datetime.timedelta(hours=gmt_offset)
                if timestamp > run_time:
                    for alerts in self.feed.data['alerts'].keys():
                        alert_times = self.feed.data['alerts'][alerts]
                        event_ts = timestamp - datetime.timedelta(days=alert_times['days'])
                        if event_ts > run_time:
                            values = dict(date=event_ts.date(), time=event_ts.time(), event=event['summary'])
                            tweet = Template(alert_times['text']).safe_substitute(values)
                            evnt = {'timestamp': str_date(event_ts), 'tweet': tweet,
                                    'id': event['id']+str_date(event_ts), 'updated': event['updated'],
                                    'processed': False}
                            tweet_manager.append(evnt)
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        tweet_manager.save()


run = GoogleFeedExtractor('/home/tim/Projects/rss-twitter/adhoc-calendar.yaml')
run.processor()


