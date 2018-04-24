from flask_restful import Resource, reqparse
from V2.Services.PageDataService import PageDataService
from V2.Services.RequestInfoService import RequestInfoService
from V2.CustomException import CustomException
from flask import jsonify
from datetime import datetime
import re
import sys

parser = reqparse.RequestParser()
parser.add_argument('company', type=str, help='Placeholder company help')
parser.add_argument('startdate', type=str)
parser.add_argument('enddate', type=str)
parser.add_argument('fields', type=str)  # needs work


class PageDataControllerV2(Resource):

    def __init__(self):
        self._page_data_service = PageDataService()
        self._request_info_service = RequestInfoService()

    def get(self):

        args = parser.parse_args()  # from my understanding should return 400 if args are not well formed (as defined above)

        page = args['company']
        start_date_string = args['startdate']
        end_date_string = args['enddate']
        fields_string = args['fields']

        if (fields_string != None):
            try:
                page_fields_string = re.sub('posts.fields\([\w,]*\)','', fields_string)
                page_fields_string = re.sub('(,\s){2,}', ',', page_fields_string)
                page_fields_string = re.sub('(^,|,$)', '', page_fields_string, )
                page_fields = page_fields_string.split(',')
            except:
                return self.error(400, 'Malformed fields parameter')

            try:
                post_section_match = re.search('posts.fields\([\w,]*\)', fields_string)
                if (post_section_match != None):
                    post_section_trimmed = post_section_match.group(0)[13:-1]
                    post_fields = post_section_trimmed.split(',')
                else:
                    post_fields = None
            except:
                return self.error(400, 'Malformed post fields'), 400

        else:
            page_fields = None
            post_fields = None

        params = {
            'page': page,
            'startdate': start_date_string,
            'enddate': end_date_string,
            'pageFields': page_fields,
            'postFields': post_fields
        }
        self._request_info_service.start(params)

        try:
            if(start_date_string != None):
                start_date = datetime.strptime(start_date_string,'%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                start_date = None
            if(end_date_string != None):
                end_date = datetime.strptime(end_date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                end_date = None
        except:
            return self.error(400, 'Datetime strings must be formatted: yyyy-MM-ddTHH:mm:ss.SSSZ'), 400

        try:
            page_data_response = self._page_data_service.get_page_data(page, start_date, end_date, page_fields, post_fields)
        except CustomException as custom_exception:
            return self.error(custom_exception.http_code, custom_exception.response_message)
        except Exception as ex:
            return self.error(500, "Unexpected exception: " + str(ex)), 500


        return self.success(page_data_response)

    def error(self, code, message):
        return {
            'Facebook Statistic Data': 'Error',
            'Request Information': self._request_info_service.get_with_error_info(code, message)
        }

    def success(self, page_data_response):
        return {
            'Facebook Statistic Data': page_data_response,
            'Request Information': self._request_info_service.get_with_success_info()
        }


