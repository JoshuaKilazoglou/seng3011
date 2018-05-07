import requests
import jsonpickle
from V2.CustomException import CustomException
import requests
from newsapi.newsapi_auth import NewsApiAuth


class NewsService:

    def __init__(self, api_key):
        self.auth = NewsApiAuth(api_key='4eea50884ef543f0ae370973bbeb2fcf')

    def get_news_articles(self, topic, category):

        try:

            parameters = {}
            parameters['q'] = topic
            parameters['language'] = 'en'
            parameters['country'] = 'au'
            parameters['sortBy'] = 'relevancy'
            parameters['pageSize'] = 25
            parameters['page'] = 2

            r = requests.get('https://newsapi.org/v2/top-headlines?', auth=self.auth, params=parameters)

            return r.json()

        except:
            raise CustomException('There was a problem getting the news articles', 500)




















