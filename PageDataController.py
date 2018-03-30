from flask_restful import Resource, reqparse
from Services.PageDataService import PageDataService
from Services.RequestInfoService import RequestInfoService
from flask import jsonify


parser = reqparse.RequestParser()
parser.add_argument('company', type=str, help='Placeholder company help')
parser.add_argument('startdate', type=str)
parser.add_argument('enddate', type=str)
parser.add_argument('fields', type=list)  # needs work


class PageDataController(Resource):

    _pageDataService = PageDataService()
    _requestInfoService = RequestInfoService()

    def get(self):
        args = parser.parse_args(strict=True)  # from my understanding should return 400 if args are not well formed (as defined above)

        company = args['company']
        startdate = args['startdate']
        enddate = args['enddate']
        fields = args['fields']

        pageDataResponse = self._pageDataService.getPageData()
        requestInfo = self._requestInfoService.getRequestInfo()
        #  Below is one way we could return the two bits of data we need, i.e. the facebook output the spec provided, and also all that other crap
        # return jsonpickle.encode({
        return jsonify({
            'Facebook Statistic Data': pageDataResponse.getDict(),
            'Request Information': requestInfo.__dict__
        })

