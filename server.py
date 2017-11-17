"""API server main file."""

from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
#  import bcrypt

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
users_collection = app.db.users
app.bcrypt_rounds = 12
api = Api(app)


class User(Resource):
    """Handle requests related to user document."""

    def post(self):
        """Add new user document in users colleciton."""
        user = request.json

        result = users_collection.insert_one(user)

        posted_user = users_collection.find_one(
            {'_id': ObjectId(result.inserted_id)}
        )

        return posted_user

    def get(self):
        """Get specified user document from users colleciton."""
        user_id = request.args.get('id')

        user = users_collection.find_one({'_id': ObjectId(user_id)})

        print(user)
        if user is None:
            return None, 404, None

        return user

    def put(self):
        """Replace user in users collection."""
        user = request.json
        user_id = request.args.get('id')

        result = users_collection.find_one_and_replace(
            {'_id': ObjectId(user_id)}, user
        )

        return result

    def patch(self):
        """Update user in users collection."""
        updated_info = request.json  # Dict containing updated key: values
        user_id = request.args.get('id')

        result = users_collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': updated_info}
        )

        return result

    def delete(self):
        """Delete user document from users collection."""
        user_id = request.args.get('id')

        result = users_collection.find_one_and_delete(
            {'_id': ObjectId(user_id)}
        )

        return result


# API Routes
api.add_resource(User, '/user')
# api.add_resource(Trips, '/user/trips')
# api.add_resource(Trip, '/user/trips/<string:trip_id>')


# Custom JSON serializer for flask_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    """Serialize flask data into JSON before response."""
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request
    # related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
