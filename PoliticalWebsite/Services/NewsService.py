from datetime import timedelta
import jsonpickle
import requests


class NewsService:

    KEY = '737bb7a0-03e3-4636-8819-d2d18664d778'

    def get_news_response(self, query, from_date, to_date):
        # dates are in format of YYYY-MM-DD

        params = {
            'from-date' : from_date,
            'to-date' : to_date,
            'show-fields': 'headline',
            'q': query,
            'api-key' : self.KEY
        }

        response_json = requests.get('https://content.guardianapis.com/search', params)
        response_object = jsonpickle.decode(response_json.text)

        return response_object