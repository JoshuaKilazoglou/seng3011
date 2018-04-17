import facebook
import requests
import jsonpickle
import sys


#############################################
#  This is where facebook graph API calls will go (and maybe other business logic)
#############################################
class PageDataService:

    _ACCESS_TOKEN = '2019883274951221|1c9281343bdcde168cdad00e354fd2aa'

    def get_page_data(self, page, start_date, end_date, page_fields, post_fields):

        params = {'fields': ','.join(page_fields), 'access_token': self._ACCESS_TOKEN}

        page_response = requests.get('https://graph.facebook.com/v2.11/' + page, params)
        page_response_dict = jsonpickle.decode(page_response.text)

        symbol, company = self.get_symbol_and_company(page)

        response = {
            'InstrumentID': symbol,
            'CompanyName': company
        }

         # print(str(page_response_dict),file=sys.stdout)

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

        if type(post_fields) is list and len(post_fields) > 0:
            response['posts'] = self.get_posts(page_id=page_response_dict['id'], start_date=start_date, end_date=end_date, fields=post_fields)

        return response

    def get_posts(self, page_id, start_date, end_date, fields):

        fields_out = ['id', 'created_time']

        for field in fields:
            if field == 'post_type':
                fields_out.append('type')
            if field == 'post_message':
                fields_out.append('message')
            if field == 'post_like_count':
                fields_out.append('likes.limit(1).summary(true)')
            if field == 'post_comment_count':
                fields_out.append('comments.limit(1).summary(true)')

        params = {
            'access_token': self._ACCESS_TOKEN,
            'since': start_date.isoformat(),
            'until': end_date.isoformat(),
            'fields': ','.join(fields_out)
        }

        api_response = requests.get('https://graph.facebook.com/v2.11/' + page_id + '/posts', params)
        api_response_dict = jsonpickle.decode(api_response.text)

        post_response = []

        for facebook_post in api_response_dict['data']:
            post = {'post_id' : facebook_post['id']}
            for field in fields:
                if field == 'post_type':
                    post[field] = facebook_post['type']
                if field == 'post_message':
                    post[field] = facebook_post['message']
                if field == 'post_like_count':
                    post[field] = facebook_post['likes']['summary']['total_count']
                if field == 'post_comment_count':
                    post[field] = facebook_post['comments']['summary']['total_count']
                if field == 'post_created_time':
                    post[field] = facebook_post['created_time']
            post_response.append(post)

        return post_response

    def get_symbol_and_company(self, page):
        params = {
            'query': page,
            'callback': 'YAHOO.Finance.SymbolSuggest.ssCallback',
            'lang': 'en'
        }

        info = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc', params)

        info_object = jsonpickle.decode(info.text[39:-2])
        first_result = info_object['ResultSet']['Result'][0]

        symbol = first_result['symbol']
        company = first_result['name']

        return symbol, company











