import json
from flask import Blueprint
from flask import make_response
from flask_restplus import Api

from flask_mongoengine import BaseQuerySet

from bson import json_util
from bson.son import SON

from apis.namespace.ptg import api as ns_obj

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint,
          title='PTG Restful API',
          version='1.0',
          description='A description',
          # other API metadatas
          )


def date_to_string(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat().split('T')[0]


@api.representation('application/json')
def output_json(data, code, headers=None):
    '''Use Bason.json_util for JSON serialization'''

    if type(data) == 'str':
        resp = make_response(data, code)
        resp.headers.extend(headers or {})
        return resp

    if isinstance(data, BaseQuerySet):
        data = data.as_pymongo()
        rows = []
        for row in data:
            rows.append(json.loads(json.dumps(row, default=date_to_string)))
        data = rows
    elif isinstance(data, SON):
        data = data.to_mongo()

    resp = make_response(json_util.dumps(data), code)
    resp.headers.extend(headers or {})

    return resp


api.add_namespace(ns_ptg_obj)
