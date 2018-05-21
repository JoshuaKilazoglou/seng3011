import jsonpickle
import os
import sys
from settings import APP_ROOT
import requests
from datetime import datetime, timedelta


class PriceEffectService:

    KEY = 'TKZU7X5L2H3WYZ9R'

    def get_price_effect(self, sector, date):

        path = os.path.join(APP_ROOT, 'PoliticalWebsite', 'Data', 'Sectors.json')
        with open(path) as eventsJson:

            sectors = jsonpickle.decode(eventsJson.read())['Sectors']
            sector_data = list(filter(lambda x: x['Name'] == sector, sectors))[0]

            short = []
            medium = []
            long = []

            for company in sector_data['Companies']:
                symbol = company['symbol']

                response_object = self.get_response_object(symbol)

                series = response_object['Time Series (Daily)']

                if date.weekday() == 5:
                    date = date + timedelta(days=2)
                elif date.weekday() == 6:
                    date = date + timedelta(days=1)

                try:
                    # short_before = self.get_surrounding_days(series, date, True, 3)
                    # short_after = self.get_surrounding_days(series, date, False, 3)
                    # medium_before = self.get_surrounding_days(series, date, True, 50)
                    # medium_after = self.get_surrounding_days(series, date, False, 50)
                    print('b', file=sys.stdout)
                    long_before = self.get_surrounding_days(series, date, True, 365)
                    long_after = self.get_surrounding_days(series, date, False, 365)
                    print('a', file=sys.stdout)
                except Exception as ex:
                    print(ex, file=sys.stdout)
                    continue


                # n_short = self.normalize_list(short_before + short_after)
                # n_medium = self.normalize_list(medium_before + medium_after)
                n_long = self.normalize_list(long_before + long_after)

                # short.append(n_short)
                # medium.append(n_medium)
                long.append(n_long)

            # short_list = self.average_lists(short)
            # medium_list = self.average_lists(medium)
            long_list = self.average_lists(long)

            s_before_avg = self.average_value(long_list[362:365])
            s_after_avg = self.average_value(long_list[365:368])
            m_before_avg = self.average_value(long_list[315:365])
            m_after_avg = self.average_value(long_list[365:415])
            l_before_avg = self.average_value(long_list[:365])
            l_after_avg = self.average_value(long_list[365:])

            s_diff = self.percentage_difference(s_before_avg, s_after_avg)
            m_diff = self.percentage_difference(m_before_avg, m_after_avg)
            l_diff = self.percentage_difference(l_before_avg, l_after_avg)

            return { "short": s_diff * 100, "medium": m_diff * 100, "long": l_diff * 100 }

    def percentage_difference(self, a, b):
        return abs(a - b) / ((a+b)/ 2)

    def average_value(self, list):
        length = len(list)
        if length == 0:
            return 0
        total = 0
        for i in range(0, length):
            total += list[i]
        return total / length

    def get_surrounding_days(self, series, date, before, range):
        modifier = 1 if before == True else -1

        curr_company_data = []
        day_count = 0
        day_difference = 0
        while day_count < range:
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


