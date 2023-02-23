from main import read_only_db
from flask import Blueprint
from flask import request
from bson.json_util import ObjectId, Int64
from flask import make_response

read_only = Blueprint('read_only', __name__)

@read_only.route('/image/<pid>', methods=['GET'])
def get_image(pid):
    data = read_only_db.get_collection('Images').find_one({'_id': ObjectId(pid)}).get('data')
    response = make_response(data)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response
