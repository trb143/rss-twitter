import json


class TweetManager():

    def __init__(self, database):
        self.database = database
        try:
            handle = open(database)
            self.tweets = json.load(handle)
            handle.close()
        except:
            self.tweets = []

    def append(self, record):
        for tweet in self.tweets:
            if tweet['id'] == record['id']:
                return
        self.tweets.append(record)

    def save(self):
        data = open(self.database, 'w')
        data.write(json.dumps(self.tweets))
        data.close()
