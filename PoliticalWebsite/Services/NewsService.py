from datetime import timedelta
import jsonpickle
import requests


class NewsService:

    KEY = '4eea50884ef543f0ae370973bbeb2fcf'

    def get_news_response(self, query, date):

        before_date = date - timedelta(days=20)
        after_date = date + timedelta(days=20)

        params = {
            'q' : query,
            'from' : before_date,
            'to' : after_date,
            'apiKey' : self.KEY
        }

        response_json = requests.get('https://newsapi.org/v2/everything?', params)
        response_object = jsonpickle.decode(response_json.text)

        return response_object
