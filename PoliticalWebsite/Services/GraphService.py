import jsonpickle
import os
import sys
from settings import APP_ROOT
import requests
from datetime import datetime, timedelta

class GraphService:

    KEY = 'TKZU7X5L2H3WYZ9R'

    def get_graph_data_by_sector(self, sector, date):

        path = os.path.join(APP_ROOT, 'PoliticalWebsite', 'Data', 'Sectors.json')
        with open(path) as eventsJson:

            sectors = jsonpickle.decode(eventsJson.read())['Sectors']
            sector_data = list(filter(lambda x: x['Name'] == sector, sectors))[0]

            data = []

            for company in sector_data['Companies']:
                symbol = company['symbol']
                params = {
                    'function': 'TIME_SERIES_DAILY',
                    'symbol': symbol,
                    'outputsize': 'full',
                    'apikey': self.KEY
                }
                response_json = requests.get('https://www.alphavantage.co/query', params)
                response_object = jsonpickle.decode(response_json.text)
                series = response_object['Time Series (Daily)']

                curr_company_data = []

                for i in range(1, 20):
                    current_date = date - timedelta(days=i)
                    dt_string = current_date.strftime('%Y-%m-%d')
                    print(dt_string, file=sys.stdout)
                    curr_company_data.insert(0, series[dt_string])

                data.append(curr_company_data)


            return data

