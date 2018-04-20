class CustomException(Exception):
    def __init__(self, message, http_code):

        # Call the base class constructor with the parameters it needs
        super(CustomException, self).__init__(message)

        self.http_code = http_code
        self.response_message = message
