import datetime
from flask_restplus import Resource, fields, Namespace
from ds_query import get_all_ds


api = Namespace('obj',
                description='operations for ptg obj')

# modes for swagger UI
object= api.model('object', {
    'name': fields.String(required=True, description='The object name'),
})


@api.route('/')
class ObjList(Resource):
    '''Shows a list of all objs'''

    def get(self):
        '''List all objects'''

        objects= sorted(get_all_target_objects())
        return objects
