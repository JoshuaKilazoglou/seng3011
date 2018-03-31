from flask_restful import Resource, reqparse, abort
from Services.PageDataService import PageDataService
from Services.RequestInfoService import RequestInfoService
from flask import jsonify, Response
from datetime import datetime


parser = reqparse.RequestParser()
parser.add_argument('company', type=str, help='Placeholder company help')
parser.add_argument('startdate', type=str)
parser.add_argument('enddate', type=str)
parser.add_argument('fields', type=str)  # needs work


class PageDataController(Resource):

    _pageDataService = PageDataService()
    _requestInfoService = RequestInfoService()

    def get(self):
        args = parser.parse_args(strict=True)  # from my understanding should return 400 if args are not well formed (as defined above)

        company = args['company']
        startdateString = args['startdate']
        enddateString = args['enddate']
        fields = args['fields'].split(',')

        try:
            startdate = datetime.strptime(startdateString,'%Y-%m-%dT%H:%M:%S.%fZ')
            enddate = datetime.strptime(enddateString, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            response = jsonify(
                {
                    'code' : 400,
                    'message': "Datetime strings must be formatted: yyyy-MM-ddTHH:mm:ss.SSSZ"
                })
            response.status_code = 400
            return response

        pageDataResponse = self._pageDataService.getPageData(company, startdate, enddate, fields)
        requestInfo = self._requestInfoService.getRequestInfo(args)

        return jsonify({
            'Facebook Statistic Data': pageDataResponse.getDict(),
            'Request Information': requestInfo.__dict__
        })

