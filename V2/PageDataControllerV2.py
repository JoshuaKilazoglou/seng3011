from flask_restful import Resource, reqparse
from V2.Services.PageDataService import PageDataService
from V2.Services.RequestInfoService import RequestInfoService
from flask import jsonify
from datetime import datetime


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

        args = parser.parse_args(strict=True)  # from my understanding should return 400 if args are not well formed (as defined above)

        page = args['company']
        start_date_string = args['startdate']
        end_date_string = args['enddate']
        fields = args['fields'].split(',')
        page_fields = None #TODO
        post_fields = None #TODO

        params = {
            'page': page,
            'startdate': start_date_string,
            'enddate': end_date_string,
            'fields': fields
        }
        self._request_info_service.start(params)

        try:
            start_date = datetime.strptime(start_date_string,'%Y-%m-%dT%H:%M:%S.%fZ')
            end_date = datetime.strptime(end_date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return self.error(400, 'Datetime strings must be formatted: yyyy-MM-ddTHH:mm:ss.SSSZ')


        #
        # ...
        #

        page_data_response = self._page_data_service.get_page_data(page, start_date, end_date, fields, post_fields)

        return self.success(page_data_response)

    def error(self, code, message):
        return jsonify({
            'Facebook Statistic Data': None,
            'Request Information': self._request_info_service.get_with_error_info(code, message)
        })

    def success(self, page_data_response):
        return jsonify({
            'Facebook Statistic Data': page_data_response,
            'Request Information': self._request_info_service.get_with_success_info()
        })


