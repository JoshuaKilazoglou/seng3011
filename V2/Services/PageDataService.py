from V2.Models.PageDataModel import PageDataModel
import facebook
import requests
import jsonpickle
import sys

#############################################
#  This is where facebook graph API calls will go (and maybe other business logic)
#############################################
class PageDataService:

    def get_page_data(self, page, start_date, end_date, page_fields, post_fields):

        access_token = '2019883274951221|1c9281343bdcde168cdad00e354fd2aa'

        params = {'fields': ','.join(page_fields), 'access_token': access_token}

        page_response = requests.get('https://graph.facebook.com/v2.11/' + page, params)
        page_response_dict = jsonpickle.decode(page_response.text)

        symbol, company = self.get_symbol_and_company(page)

        response = {
            'InstrumentID': symbol,
            'CompanyName': company
        }

        for field in page_fields:
            if field == 'id':
                response['PageId'] = page_response_dict['id']
            elif field == 'name':
                response['PageName'] = page_response_dict['name']
            elif field == 'website':
                response['Website'] = page_response_dict['website']
            elif field == 'description':
                response['Description'] = page_response_dict['description']
            elif field == 'category':
                response['Category'] = page_response_dict['category']
            elif field == 'fan_count':
                response['FanCount'] = page_response_dict['fan_count']

        if post_fields is list and len(post_fields) > 0:
            response.posts = self.get_posts(id=page_response_dict['id'], start_date = start_date, end_date = end_date, fields = post_fields)

        return response

    def get_posts(self, id, start_date, end_date, fields):

        params = {}

        posts_response = requests.get('https://graph.facebook.com/v2.11/' + id + '/posts', params)

        return posts_response

    def get_symbol_and_company(self, page):
        params = {
            'query': page,
            'callback': 'YAHOO.Finance.SymbolSuggest.ssCallback',
            'lang': 'en'
        }

        info = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc', params)
        print(info.text[39:-2], file=sys.stdout)

        info_object = jsonpickle.decode(info.text[39:-2])
        first_result = info_object['ResultSet']['Result'][0]

        symbol = first_result['symbol']
        company = first_result['name']

        return symbol, company











