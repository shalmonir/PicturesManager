import bleach

from src.Utils.RequestProcessor import REQUEST_USER_NAME, REQUEST_USER_PHRASE


class AuthInputSanitizer:
    @staticmethod
    def sanitize_login_request(login_request):
        return {REQUEST_USER_PHRASE: bleach.clean(login_request[REQUEST_USER_PHRASE]),
                REQUEST_USER_NAME: bleach.clean(login_request[REQUEST_USER_NAME])}
