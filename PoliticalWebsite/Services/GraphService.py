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

                response_object = self.get_response_object(symbol)

                series = response_object['Time Series (Daily)']

                if date.weekday() == 5:
                    print('fri', file=sys.stdout)
                    date = date + timedelta(days=2)
                elif date.weekday() == 6:
                    print('fri', file=sys.stdout)
                    date = date + timedelta(days=1)

                try:
                    before_data = self.get_surrounding_days(series, date, before=True)
                    day_of = float(series[date.strftime('%Y-%m-%d')]['4. close'])
                    after_data = self.get_surrounding_days(series, date, before=True)
                except Exception as ex:
                    print(ex, file=sys.stdout)
                    continue

                all_data = before_data + [day_of] + after_data
                normalized_data = self.normalize_list(all_data)
                data.append(normalized_data)

            return self.average_lists(data)

    def get_surrounding_days(self, series, date, before):
        modifier = 1 if before == True else -1

        curr_company_data = []
        day_count = 0
        day_difference = 0
        while day_count < 20:
            day_difference += 1 * modifier
            current_date = date - timedelta(days=day_difference)
            dt_string = current_date.strftime('%Y-%m-%d')
            try:
                day_data = series[dt_string]
            except:
                continue
            close_value = float(day_data['4. close'])
            curr_company_data.insert(0, close_value)
            day_count += 1

        return curr_company_data


    def get_response_object(self, symbol):
        path = os.path.join(APP_ROOT, 'PoliticalWebsite', 'Data', 'Prices.json')
        with open(path) as prices_file:
            prices = jsonpickle.decode(prices_file.read())

            if symbol in prices['companies']:
                data = prices['companies'][symbol]
                return data
            else:
                params = {
                    'function': 'TIME_SERIES_DAILY',
                    'symbol': symbol,
                    'outputsize': 'full',
                    'apikey': self.KEY
                }
                response_json = requests.get('https://www.alphavantage.co/query', params)
                response_object = jsonpickle.decode(response_json.text)

        with open(path, 'w') as prices_file:
            prices['companies'][symbol] = response_object
            json_output = jsonpickle.encode(prices)
            prices_file.write(json_output)

        return response_object

    def normalize_list(self, list_in):
        max_val = max(n for n in list_in)
        min_val = min(n for n in list_in)
        normalized_list = list(map(lambda n: (n - min_val) / (max_val - min_val), list_in))
        return normalized_list

    def average_lists(self, list_of_lists):
        list_length = len(list_of_lists[0])
        result = [0] * list_length
        for i in range(0, list_length):
            for curr_list in list_of_lists:
                result[i] += curr_list[i]
        return list(map(lambda x: x / len(list_of_lists), result))


