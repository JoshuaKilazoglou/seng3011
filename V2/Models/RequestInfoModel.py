from datetime import datetime

class RequestInfoModel:
    def __init__(self):
        self.start_request()

        self.team_name = "laser"
        self.module_name = "pageData"
        self.module_version = "v2"
        self.parameters = None
        self.start_date_time = None
        self.end_date_time = None
        self.time_elapsed = None
        self.output_file_name = "pageData.json"

    def finish_request(self):
        self.end_date_time = datetime.now()
        self.time_elapsed = self.start_date_time = self.end_date_time

    def start_request(self):
        self.start_date_time = datetime.now()

