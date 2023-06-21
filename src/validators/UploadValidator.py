from src.Utils.RequestProcessor import REQUEST_UPLOAD_NAME, REQUEST_UPLOAD_FILES


class UploadValidator:
    @staticmethod
    def validate(request):
        if not request[REQUEST_UPLOAD_NAME] or not request[REQUEST_UPLOAD_FILES]:
            return False
