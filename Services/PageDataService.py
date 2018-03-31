from Models.PageDataModel import PageDataModel, PostModel
import facebook
import requests
import jsonpickle

#############################################
#  This is where facebook graph API calls will go (and maybe other business logic)
#############################################
class PageDataService:

    def getPageData(self, company, startdate, enddate, fields):

        access_token = '2019883274951221|1c9281343bdcde168cdad00e354fd2aa'

        params = {'fields': ','.join(fields), 'access_token': access_token}
        response = requests.get('https://graph.facebook.com/v2.11/' + company, params)
        responseDict = jsonpickle.decode(response.text)

        pageData = PageDataModel()
        pageData.pageId = responseDict['id'] if 'id' in fields else None,
        pageData.companyName = responseDict['name'] if 'name' in fields else None,
        pageData.instrumentID = 'Unknown',
        pageData.pageName = responseDict['name'] if 'name' in fields else None,
        pageData.website = responseDict['website'] if 'website' in fields else None,
        pageData.description = responseDict['description'] if 'description' in fields else None,
        pageData.category = responseDict['category'] if 'category' in fields else None,
        pageData.fan_count = responseDict['fan_count'] if 'fan_count' in fields else None,
        pageData.posts = None

        return pageData

    def fields(self):
        # Setting up the API. Graph is our access point to grab information
        ACCESS_TOKEN = "EAACEdEose0cBAHEzkmxSLzi3O7upORZB1rTnPqBQDRclWRNFkdBFglVw15MjR1vCWTPmc5qekkj2o2aOY5efgZAPKa5xmCQmiIZBuquI2CD4xhVdzoZBt38PGy1BsnZBtjhCckpZARXnHAAj9EvjSe0ZBGZC6C0iZBJzRPaROjyZCbJZAlG27Cxy4bZBukThYikObzpAZBGq7EvOTuQZDZD"
        graph = facebook.GraphAPI(ACCESS_TOKEN)

        # For now using dummy companies/fields to show how it works
        company = "820882001277849"  # Coca-Cola
        fields = ['id', 'name']

        # building the request. Always start with company and prepare to query fields
        request = company + "?fields="

        # append fields
        for field in fields:
            request = request + field + ","

        # remove last comma
        request = request[:-1]

        # data is a dict containing the return frmo the api
        data = graph.request(request)

        return data

    def posts(selfs):
        ACCESS_TOKEN = "EAACEdEose0cBAHEzkmxSLzi3O7upORZB1rTnPqBQDRclWRNFkdBFglVw15MjR1vCWTPmc5qekkj2o2aOY5efgZAPKa5xmCQmiIZBuquI2CD4xhVdzoZBt38PGy1BsnZBtjhCckpZARXnHAAj9EvjSe0ZBGZC6C0iZBJzRPaROjyZCbJZAlG27Cxy4bZBukThYikObzpAZBGq7EvOTuQZDZD"
        graph = facebook.GraphAPI(ACCESS_TOKEN)

        company = "820882001277849"  # Coca-Cola

        # there's quite a few date formats we can use
        startDate = "4feb2018"
        endDate = "now"

        # limit the number of posts for processing sake. Can remove if we don't want it there
        limit = "20"

        request = company + "/posts?since=" + startDate + "&until=" + endDate + "&limit=" + limit

        data = graph.request(request)

        return data











