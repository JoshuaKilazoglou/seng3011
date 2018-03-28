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

