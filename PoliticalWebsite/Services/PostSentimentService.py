import jsonpickle
import os
import sys
from settings import APP_ROOT
import requests
from datetime import datetime, timedelta
from textblob import TextBlob


class PostSentimentService:

    _ACCESS_TOKEN = '2019883274951221|1c9281343bdcde168cdad00e354fd2aa'

    def get_sentiment_by_sector(self, sector, date):

        path = os.path.join(APP_ROOT, 'PoliticalWebsite', 'Data', 'Sectors.json')

        with open(path) as eventsJson:

            sectors = jsonpickle.decode(eventsJson.read())['Sectors']
            sector_data = list(filter(lambda x: x['Name'] == sector, sectors))[0]
            for company in sector_data['Companies']:

                page = company['facebook']
                if page == '': continue

                response_before = self.get_response_before(page, date)
                response_after = self.get_response_after(page, date)

                if 'error' in response_before: continue

                messages_before = self.get_messages(response_before)
                messages_after = self.get_messages(response_after)

                mb_sentiment_sum = 0
                ma_sentiment_sum = 0

                for m in messages_before:
                    tb = TextBlob(m)
                    mb_sentiment_sum += tb.sentiment.polarity

                for m in messages_after:
                    ta = TextBlob(m)
                    ma_sentiment_sum += ta.sentiment.polarity

                mb_sentiment = mb_sentiment_sum / len(messages_before) if len(messages_before) > 0 else 0
                ma_sentiment = ma_sentiment_sum / len(messages_after) if len(messages_after) > 0 else 0

        return {
            "before": mb_sentiment,
            "after": ma_sentiment
        }

    def get_messages(self, post_response):
        posts = post_response['data']
        posts_with_messages = list(filter(lambda x: 'message' in x, posts))
        post_messages = list(map(lambda x: x['message'], posts_with_messages))
        return post_messages

    def get_response_before(self, page, date):
        params = {
            'access_token': self._ACCESS_TOKEN,
            'since': (date - timedelta(days=20)).strftime('%Y-%m-%d'),
            'until': date.strftime('%Y-%m-%d')
        }
        response_json = requests.get('https://graph.facebook.com/v2.11/' + page + '/posts', params)
        response_object = jsonpickle.decode(response_json.text)

        return response_object

    def get_response_after(self, page, date):
        params = {
            'access_token': self._ACCESS_TOKEN,
            'since': date.strftime('%Y-%m-%d'),
            'until':  (date + timedelta(days=20)).strftime('%Y-%m-%d')
        }
        response_json = requests.get('https://graph.facebook.com/v2.11/' + page + '/posts', params)
        response_object = jsonpickle.decode(response_json.text)

        return response_object




