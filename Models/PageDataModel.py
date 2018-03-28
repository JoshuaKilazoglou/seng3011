#  very rough implementation

class PageDataModel:

    #  TODO make this less hacky and horrible
    def getDict(self):
        postDicts = []
        for p in self.posts:
            postDicts.append(p.__dict__)
        return {
            'pageId': self.pageId,
            'instrumentIDs': "",
            'companyNames': "",
            'pageName': "",
            'website': "",
            'description': "",
            'category': "",
            'fan_count': "",
            'posts': postDicts
        }

    pageId = ""
    instrumentIDs = ""  # What the hell is an instrumentId anyway?
    companyNames = ""  # Isn't a page associated with a single company?
    pageName = ""
    website = ""
    description = ""
    category = ""
    fan_count = ""
    posts = []


class PostModel:
    post_id = ""
    post_type = ""
    post_message = ""
    post_created_time = ""
    post_comment_coun = ""

