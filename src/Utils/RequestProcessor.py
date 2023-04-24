import logging

from flask import Request


class ProcessRequestException(Exception):
    def __init__(self):
        message = 'error processing user request'
        super().__init__(message)


class RequestProcessor:
    @staticmethod
    def process_upload_request(user_request: Request) -> dict:
        try:
            return {'files': user_request.files.getlist("file"), 'album_name': user_request.form['album_name']}
        except Exception as e:
            logging.ERROR('upload input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_login_request(login_request: Request) -> dict:
        try:
            return {'password': login_request.form["password"], 'username': login_request.form['username']}
        except Exception as e:
            logging.ERROR('login input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_search_request(search_request: Request) -> dict:
        try:
            return {'album_keyword': search_request.form["album_keyword"]}
        except Exception as e:
            logging.ERROR('login input error: ' + str(e))
            raise ProcessRequestException()

    @staticmethod
    def process_register_request(register_request: Request) -> dict:
        try:
            return {'password': register_request.form["password"], 'email': register_request.form['email'],
                    'name': register_request.form['name']}
        except Exception as e:
            logging.ERROR('register input error: ' + str(e))
            raise ProcessRequestException()