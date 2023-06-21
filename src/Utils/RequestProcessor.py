import logging

from flask import Request

ALBUM_KEYWORD = 'album_keyword'

REQUEST_UPLOAD_NAME = 'upload_name'
REQUEST_UPLOAD_FILES = 'file'
REQUEST_USER_NAME = 'username'
REQUEST_USER_PHRASE = 'user_phrase'
REQUEST_USER_EMAIL = 'email'

REQUEST_DATA_PHRASE = 'data_phrase'
REQUEST_DATA_COLLECTION = 'collection'
REQUEST_DATA_POST_PAYLOAD = 'post_payload'


class ProcessRequestException(Exception):
    def __init__(self):
        message = 'error processing user request'
        super().__init__(message)


class RequestProcessor:
    @staticmethod
    def process_upload_request(user_request: Request) -> dict:
        try:
            return {REQUEST_UPLOAD_FILES: user_request.files.getlist(REQUEST_UPLOAD_FILES),
                    REQUEST_UPLOAD_NAME: user_request.form[REQUEST_UPLOAD_NAME]}
        except Exception as e:
            logging.ERROR(f"upload input error: {e}")
            raise ProcessRequestException()

    @staticmethod
    def process_login_request(login_request: Request) -> dict:
        try:
            return {REQUEST_USER_PHRASE: login_request.form[REQUEST_USER_PHRASE],
                    REQUEST_USER_NAME: login_request.form[REQUEST_USER_NAME]}
        except Exception as e:
            logging.ERROR('login input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_search_request(search_request: Request) -> dict:
        try:
            return {ALBUM_KEYWORD: search_request.form[ALBUM_KEYWORD]}
        except Exception as e:
            logging.ERROR('login input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_register_request(register_request: Request) -> dict:
        try:
            return {REQUEST_USER_PHRASE: register_request.form[REQUEST_USER_PHRASE], REQUEST_USER_EMAIL: register_request.form[REQUEST_USER_EMAIL],
                    REQUEST_USER_NAME: register_request.form[REQUEST_USER_NAME]}
        except Exception as e:
            logging.ERROR('register input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_data_request(data_request: Request) -> dict:
        try:
            return {REQUEST_DATA_PHRASE: data_request[REQUEST_DATA_PHRASE],
                    REQUEST_DATA_COLLECTION: data_request[REQUEST_DATA_COLLECTION]}
        except Exception as e:
            logging.ERROR('register input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_data_update_request(data_update_request: Request) -> dict:
        try:
            return {REQUEST_DATA_PHRASE: data_update_request[REQUEST_DATA_PHRASE],
                    REQUEST_DATA_COLLECTION: data_update_request[REQUEST_DATA_COLLECTION],
                    REQUEST_DATA_POST_PAYLOAD: data_update_request[REQUEST_DATA_COLLECTION]}
        except Exception as e:
            logging.ERROR('register input error: ' + str(e))
            raise ProcessRequestException()

