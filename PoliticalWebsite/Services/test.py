from V2.CustomException import CustomException
import requests
import jsonpickle

def get_news_articles(q, from_date, to_date):

    params = {
        'from-date': from_date,
        'to-date': to_date,
        'show-fields': 'headline',
        'q': q,
        'apiKey': '737bb7a0-03e3-4636-8819-d2d18664d778'
    }

    page_response = requests.get("https://content/guardianapis.com/search?", params)
    page_response_dict = jsonpickle.decode(page_response.text)
    print(page_response_dict)


get_news_articles('football', "2016-10-01", "2016-12-01")


