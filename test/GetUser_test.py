import unittest
import azure.functions as func
import json
import datetime

from GetUser import main # import the method we want to test


user_id = 'Max.Mustermann@test.org'
user_surname = 'Max'
user_lastname = 'Mustermann'
user_password = 'Start1234!'
user_role = 'Admin'


class TestGetUser(unittest.TestCase):
    def test_get_user_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetUser',
            params={'user_id': user_id},
            body=None
        )

        user = func.DocumentList(
            [
                func.Document(
                    {
                        'id': user_id,
                        'surname': user_surname,
                        'lastname': user_lastname,
                        'password': user_password,
                        'role': user_role
                    }
                )
            ]
        )

        # Act
        response = main(request, user)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json['id'] == user_id
        assert response_json['surname'] == user_surname
        assert response_json['lastname'] == user_lastname
        assert response_json['password'] == user_password
        assert response_json['role'] == user_role


    def test_get_user_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetUser',
            params={},
            body=None
        )

        user = func.DocumentList(initlist=None)

        # Act
        response = main(request,user)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please provide a user_id parameter.' in response.get_body().decode()


    def test_get_user_wrongparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetUser',
            params={'user_id': user_id},
            body=None
        )

        user = func.DocumentList(initlist=None)

        # Act
        response = main(request,user)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert f'Could not find user with the ID {user_id}.' in response.get_body().decode()