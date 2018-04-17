#  very rough implementation

class PageDataModel:

    #  TODO make this less hacky and horrible
    def getDict(self):
        postDicts = []
        if(self.posts is not None):
            for p in self.posts:
                postDicts.append(p.__dict__)
        return {
            'pageId': self.pageId[0],
            'instrumentID': self.instrumentID[0],
            'companyName': self.companyName[0],
            'pageName': self.pageName[0],
            'website': self.website[0],
            'description': self.description[0],
            'category': self.category[0],
            'fan_count': self.fan_count[0],
            'posts': postDicts
        }

    pageId = ""
    instrumentID = ""  # What the hell is an instrumentId anyway?
    companyName = ""  # Isn't a page associated with a single company?
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

