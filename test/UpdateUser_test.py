import unittest
import azure.functions as func
import json

from UpdateUser import main # import the method we want to test
from unittest import mock

user_id = '45345-543dsds-543543fds-fdsf7af90asf-45345'
user_password = 'passw0rd'
user_password_updated = 'savepassw0rd'
user_surname = 'Surname'
user_surname_updated = 'UpdatedSurname'
user_lastname = 'lastname'
user_lastname_updated = 'Huber'
user_role = 'user'
user_role_updated = 'administrator'

    

class TestUdpateUser(unittest.TestCase):
    def test_update_user_correct(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateUser',
            params={
                'user_id': user_id
            },
            body=json.dumps(
                {
                    'password': user_password_updated,
                    'surname': user_surname_updated,
                    'lastname': user_lastname_updated,
                    'role': user_role_updated
                }
            ).encode('utf8')
        )

        user = func.DocumentList(
            [
                func.Document(
                    {
                        'id': user_id,
                        'password': user_password,
                        'surname': user_surname,
                        'lastname': user_lastname,
                        'role': user_role
                    }
                )
            ]
        )

        outuser = mock.Mock()
        
        # Act
        response = main(request, user, outuser)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outuser.mock_calls[0][1][0].data['id'] == user_id
        assert outuser.mock_calls[0][1][0].data['password'] == user_password_updated
        assert outuser.mock_calls[0][1][0].data['surname'] == user_surname_updated
        assert outuser.mock_calls[0][1][0].data['lastname'] == user_lastname_updated
        assert outuser.mock_calls[0][1][0].data['role'] == user_role_updated


    def test_update_user_noparam(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateUser',
            params={},
            body=json.dumps(
                {
                    'password': user_password_updated,
                    'surname': user_surname_updated,
                    'lastname': user_lastname_updated,
                    'role': user_role_updated
                }
            ).encode('utf8')
        )

        user = func.DocumentList(initlist=None)

        outuser = mock.Mock()
        
        # Act
        response = main(request, user, outuser)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response
        assert f"Please provide a user ID to query for." in response.get_body().decode()


    def test_update_user_nobody(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateUser',
            params={
                'user_id': user_id
            },
            body=None
        )

        user = func.DocumentList(
            [
                func.Document(
                    {
                        'id': user_id,
                        'password': user_password,
                        'surname': user_surname,
                        'lastname': user_lastname,
                        'role': user_role
                    }
                )
            ]
        )

        outuser = mock.Mock()
        
        # Act
        response = main(request, user, outuser)

        # Assert
        # Assert status code
        assert response.status_code == 500


    def test_update_user_wrongparam(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateUser',
            params={
                'user_id': user_id
            },
            body=json.dumps(
                {
                    'password': user_password_updated,
                    'surname': user_surname_updated,
                    'lastname': user_lastname_updated,
                    'role': user_role_updated
                }
            ).encode('utf8')
        )

        user = func.DocumentList(initlist=None)

        outuser = mock.Mock()
        
        # Act
        response = main(request, user, outuser)

        # Assert
        # Assert status code
        assert response.status_code == 404

        # Assert the CosmosDB output binding is working correctly
        assert f"user not found" in response.get_body().decode()


