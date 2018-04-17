from V2.Models.RequestInfoModel import RequestInfoModel


class RequestInfoService:

    def __init__(self):
        self.request_info_model = RequestInfoModel()

    def start(self, parameters):
        self.request_info_model.parameters = parameters
        self.request_info_model.start_request()

    def get_with_error_info(self, code, message):
        return {
            'DevTeam': self.request_info_model.team_name,
            'ModuleName': self.request_info_model.module_name,
            'ModuleVersion': self.request_info_model.module_version,
            'Parameters': self.request_info_model.parameters,
            'Successful': False,
            'ErrorDetails': {
                'Code': code,
                'Message': message
            }
        }

    def get_with_success_info(self):
        self.request_info_model.finish_request()
        return {
            'DevTeam': self.request_info_model.team_name,
            'ModuleName': self.request_info_model.module_name,
            'ModuleVersion': self.request_info_model.module_version,
            'Parameters': self.request_info_model.parameters,
            'Successful': True,
            'Details': {
                'StartDateTime': self.request_info_model.start_date_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'EndDateTime': self.request_info_model.end_date_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'ElapsedTime': str(self.request_info_model.seconds_elapsed) + ' seconds',
                'OutputFileName': self.request_info_model.output_file_name
            }
        }

