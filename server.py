"""App API server main file."""

from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
# from bson.objectid import ObjectId
#  import bcrypt

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
app.bcrypt_rounds = 12
api = Api(app)


class User(Resource):
    """User resource that handles all requests related to user."""

    def post(self):
        """Add new user document to users collection."""
        new_user = request.json

        users_collection = app.db.users

        result = users_collection.insert_one(new_user)

        return "User {} was added yuuuh".format(result.inserted_id)

    def get(self):
        """Get specified user document."""
        users_collection = app.db.users

        name = request.args.get("name")

        response = users_collection.find_one({"name": name})

        return response

    def delete(self):
        """Delete specified user object in from users collection."""
        name = request.args.get("name")

        users_collection = app.db.users

        response = users_collection.delete_one({"name": name})
        print(response)

        return "{} was deleted yuuuh".format(name)

    def put(self):
        """Replace user document with new user."""
        name = request.args.get("name")

        users_collection = app.db.users

        response = users_collection.find_one_and_replace(
            {"name": name},
            {"name": "gucci mane"}
        )
        print(response)

        return "{} was replaced yuuuh".format(name)


# API Routes
api.add_resource(User, '/user')
# api.add_resource(Trip, '/user/trips', '/trips/<string:trip_id>')


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
