import json

from flask import Blueprint, request
from flask import Response

from src.Configuration.Configuration import DATA_ACCESS_PHRASE
from src.Context.AWSContext import AWSContext
from src.Utils.RequestProcessor import RequestProcessor, REQUEST_DATA_PHRASE, REQUEST_DATA_COLLECTION

data_api = Blueprint('analyze', import_name=__name__)
context = AWSContext()


@data_api.route('/get_collection_data', methods=['POST'])
def get_with_metadata():
    try:
        data_request = RequestProcessor.process_data_request(json.loads(request.data.decode()))
        if data_request.get(REQUEST_DATA_PHRASE) != DATA_ACCESS_PHRASE:
            return Response("{'Failed':'Wrong Password'}", status=401, mimetype='application/json')
        pictures = context.get_db_utility().get_pictures_by_album(data_request[REQUEST_DATA_COLLECTION])
        result = []
        for pic in pictures:
            result.append({"id": pic.id,
                           "data": pic.data,
                           "file_name": pic.file_name,
                           "path": pic.path,
                           })
        return Response(response=json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        error_response = [{"error": 'internal', "exception": str(e)}]
        return Response(response=json.dumps(error_response), status=500, mimetype='application/json')

