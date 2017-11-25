"""Unit tests for server User & Trip requests."""
import server
import unittest
import json
# import bcrypt
# import base64
from pymongo import MongoClient


class TripPlannerUserTestCase(unittest.TestCase):
    """TripPlanner User testing."""

    def setUp(self):
        """Prepare server and database for testing."""
        self.app = server.app.test_client()

        server.app.config['TESTING'] = True

        mongo = MongoClient('localhost', 27017)
        global db

        server.app.bcrypt_rounds = 4

        db = mongo.trip_planner_test
        server.app.db = db

        db.drop_collection('users')

    def testGetUser(self):
        """Test GET request for User resource."""
        self.app.post('/user',
                      headers=None,
                      data=json.dumps(dict(
                          name='Eliel Gordon',
                          email='eliel@example.com'
                        )),
                      content_type='application/json')

        response = self.app.get('/user',
                                query_string=dict(email='eliel@example.com'))

        json_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['email'], 'eliel@example.com')

    def testPostUser(self):
        """Test POST request for user."""
        response = self.app.post('/user',
                                 headers=None,
                                 data=json.dumps(dict(
                                    name="Egon Johnson",
                                    email="egon@example.com"
                                 )),
                                 content_type='application/json')

        json_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['email'], 'egon@example.com')

    def testDeleteUser(self):
        """Test DEL request for User resource."""
        self.app.post('/user',
                      headers=None,
                      data=json.dumps(dict(
                          name="Delete Me",
                          email="del@example.com"
                        )),
                      content_type='application/json')

        response = self.app.delete('/user',
                                   query_string=dict(email="del@example.com"))

        self.assertEqual(response.status_code, 200)


class TripPlannerTripTestCase(unittest.TestCase):
    """TripPlanner Trip testing."""

    def setUp(self):
        """Prepare server and database for testing."""
        self.app = server.app.test_client()

        server.app.config['TESTING'] = True

        mongo = MongoClient('localhost', 27017)
        global db

        server.app.bcrypt_rounds = 4

        db = mongo.trip_planner_test
        server.app.db = db

        db.drop_collection('users')

    def testGetTrip(self):
        """Test GET request for Trip resource."""
        self.app.post('/user',
                      headers=None,
                      data=json.dumps(dict(
                          email='trips@example.com',
                          trips=[
                            dict(
                                name='2018 Vacation WOOOO',
                                waypoints=[
                                    'Alaska',
                                    'Yee',
                                    'That',
                                    'Place'
                                ],
                                completed=False
                            )
                          ]
                        )),
                      content_type='application/json'
                      )

        response = self.app.get('/user/trips',
                                query_string=dict(email='trips@example.com'))

        json_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response[-1]['name'], '2018 Vacation WOOOO')

    def testPostTrip(self):
        """Test POST request for Trip resource."""
        response = self.app.post('/user/trips?email=trips@example.com',
                                 headers=None,
                                 data=json.dumps(
                                        dict(
                                            name='2018 Vacation WOOOO',
                                            waypoints=[
                                                'Alaska',
                                                'Yee',
                                                'That',
                                                'Place'
                                            ],
                                            completed=False
                                        )
                                    ),
                                 content_type='application/json'
                                 )

        json_response = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['email'], 'trips@example.com')

    def testDeleteTrip(self):
        """Test DEL request for Trip resource."""
        pass


if __name__ == '__main__':
    unittest.main()
