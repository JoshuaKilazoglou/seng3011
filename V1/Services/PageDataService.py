from V1.Models.PageDataModel import PageDataModel
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











