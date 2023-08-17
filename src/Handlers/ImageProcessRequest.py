import json
import os

import requests

from src.Utils.RequestProcessor import RequestProcessor


class ImageProcessRequest:
    @staticmethod
    def send_request(face_recognition_request):
        file = r'E:\dev\Pictures\20200127_151827.jpg'
        url = 'http://127.0.0.1:5000/detect_faces'

        payload = {"param_1": "value_1", "param_2": "value_2"}
        files = {
            'body': (face_recognition_request['body'], json.dumps(payload), 'application/json'),
            'picture': (os.path.basename(face_recognition_request['picture']), open(face_recognition_request['picture'],
                                                                                    'rb'), 'application/octet-stream')
        }

        response = requests.post(url, files=files)
        return response.content


_input = {'body': 'nothing', 'picture': r'E:\dev\Pictures\20200127_151827.jpg'}
res = ImageProcessRequest.send_request(RequestProcessor.process_detect_faces_request(_input))
# print(res)