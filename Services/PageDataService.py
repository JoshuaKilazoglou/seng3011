from Models.PageDataModel import PageDataModel, PostModel

#############################################
#  This is where facebook graph API calls will go (and maybe other business logic)
#############################################
class PageDataService:

    # main method, returns a single "PageDataModel" object
    def getPageData(self):
        #  dummy data for now

        post1 = PostModel()
        post2 = PostModel()

        post1.post_id = '1',
        post1.post_type = 'video'
        post1.post_message = 'cool video'
        post1.post_created_time = '1/2/2001'
        post1.post_comment_coun = '1223'

        post2.post_id = '2',
        post2.post_type = 'text'
        post2.post_message = 'cool text'
        post2.post_created_time = '1/2/2008'
        post2.post_comment_coun = '222'

        response = PageDataModel()
        response.pageId = "Id",
        response.companyNames = ['Name1']
        response.instrumentIDs = ['InstrumentId1']
        response.pageName = 'page name'
        response.website = 'www.pornhub.com'
        response.description = 'a cool page'
        response.fan_count = 123123
        response.posts = [post1, post2]

        return response

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











