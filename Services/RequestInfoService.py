from Models.RequestInfoModel import RequestInfoModel

class RequestInfoService:
    # Just gets the additional log and request info that the spec asks for
    def getRequestInfo(selfs, parameters):
        requestInfoModel = RequestInfoModel()

        requestInfoModel.team = 'Laser'
        requestInfoModel.moduleName = 'PageData'
        requestInfoModel.moduleVersion = 'v1'
        requestInfoModel.parameters = parameters

        return requestInfoModel

