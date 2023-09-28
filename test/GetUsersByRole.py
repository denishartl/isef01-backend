import unittest
import azure.functions as func
import json

from GetUsersByRole import main # import the method we want to test


user_id_1 = 'Max.Mustermann@test.org'
user_surname_1 = 'Max'
user_lastname_1 = 'Mustermann'
user_role_1 = 'User'

user_id_2 = 'Jane.Doe@test.org'
user_surname_2 = 'Jane'
user_lastname_2 = 'Doe'
user_role_2 = 'User'



class TestGetUsersByRole(unittest.TestCase):
    def test_get_users_by_role_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetUsersByRole',
            params={"role": "user"},
            body=None
        )

        users = func.DocumentList(
            [
                func.Document(
                    {
                        'id': user_id_1,
                        'surname': user_surname_1,
                        'lastname': user_lastname_1,
                        'role': user_role_1
                    }
                ),
                func.Document(
                    {
                        'id': user_id_2,
                        'surname': user_surname_2,
                        'lastname': user_lastname_2,
                        'role': user_role_2
                    }
                )
            ]
        )

        # Act
        response = main(request, users)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json[0]['id'] == user_id_1
        assert response_json[0]['surname'] == user_surname_1
        assert response_json[0]['lastname'] == user_lastname_1
        assert response_json[0]['role'] == user_role_1

        assert response_json[1]['id'] == user_id_2
        assert response_json[1]['surname'] == user_surname_2
        assert response_json[1]['lastname'] == user_lastname_2
        assert response_json[1]['role'] == user_role_2

    
    def test_get_users_by_role_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetUsersByRole',
            params={},
            body=None
        )

        users = func.DocumentList(initlist=None)

        # Act
        response = main(request, users)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please provide a role to query for.' in response.get_body().decode()


    def test_get_users_by_role_noresults(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetUsersByRole',
            params={"role": "user"},
            body=None
        )

        users = func.DocumentList(initlist=None)

        # Act
        response = main(request, users)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        assert 'Found no users with this role.' in response.get_body().decode()