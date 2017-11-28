"""API server main file."""

from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import pdb
import bcrypt

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
users_collection = app.db.users
app.bcrypt_rounds = 12
api = Api(app)


class User(Resource):
    """Handle requests related to user document."""

    def post(self):
        """Add new user document to users colleciton."""
        username = request.authorization.username
        password = request.authorization.password

        encodedPassword = password.encode('utf-8')

        hashed = bcrypt.hashpw(
            encodedPassword, bcrypt.gensalt(app.bcrypt_rounds)
        ).decode()

        result = users_collection.insert_one(
            {"email": username, "password": hashed, "trips": []})

        posted_user = users_collection.find_one(
            {'_id': ObjectId(result.inserted_id)}
        )

        return (posted_user, 201, None)

    def get(self):
        """Get specified user document from users colleciton."""
        # pdb.set_trace()
        username = request.authorization.username
        password = request.authorization.password

        user = users_collection.find_one({'email': username})

        if user is None:
            return None, 404, None

        encodedPassword = password.encode('utf-8')

        # Method 2: Use checkpw
        if bcrypt.checkpw(encodedPassword, user['password'].encode('utf-8')):
            return (user, 200, None)
        else:
            return (None, 401, None)


    def put(self):
        """Replace user in users collection."""
        user = request.json
        email = request.args.get('email')

        result = users_collection.find_one_and_replace(
            {'emal': email}, user
        )

        return result

    def patch(self):
        """Update user in users collection."""
        updated_info = request.json  # Dict containing updated key: values
        email = request.args.get('email')

        result = users_collection.find_one_and_update(
            {'email': email},
            {'$set': updated_info}
        )

        return result

    def delete(self):
        """Delete user document from users collection."""
        email = request.args.get('email')

        result = users_collection.find_one_and_delete(
            {'email': email}
        )

        return result


class Trip(Resource):
    """Handle requests related to trip objects."""

    def post(self):
        """Add new trip object to user."""
        trip = request.json
        email = request.args.get('email')

        result = users_collection.find_one_and_update(
            {'email': email},
            {'$push': {'trips': trip}}
        )

        return (result, 201, None)

    def get(self):
        """Get specified trip object from user."""
        email = request.args.get('email')

        user = users_collection.find_one({'email': email})

        return user["trips"]

    def put(self):
        """Replace trip object in user."""
        trip = request.json
        email = request.args.get('email')
        trip_index = request.args.get('trip_index')

        result = users_collection.find_one_and_update(
            {'email': email},
            {'$set': {"trips." + trip_index: trip}}
        )

        return result

    def patch(self):
        """Update trip object in user."""
        self.put()

    def delete(self):
        """Delete trip object from user."""
        email = request.args.get('email')
        trip_name = request.args.get('trip_name')

        result = users_collection.find_one_and_update(
            {'email': email},
            {'$pull': {'trips': {'name': trip_name}}}
        )

        return result


# API Routes
api.add_resource(User, '/user')
api.add_resource(Trip, '/user/trips')
# api.add_resource(Trip, '/user/trips/<string:trip_index>')


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
