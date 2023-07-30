import unittest
import azure.functions as func
import json

from GetAttachments import main # import the method we want to test
from unittest import mock

ticket_id = 'testing_id_do_not_delete'
name = 'for_testing_do_not_delete.ico'
uuid = '52556c2c-28bb-11ee-a541-4ead18658f42'
blob_link = 'https://iuisef01b10e.blob.core.windows.net/attachment/52556c2c-28bb-11ee-a541-4ead18658f42'
id = 'ede37445-7aaf-4df3-802c-f590720f7626'
    

class TestGetAttachment(unittest.TestCase):
    def test_get_attachments_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachments',
            params={
                'ticket_id': ticket_id
            },
            body=None
        )

        attachments = func.DocumentList(
            [
                func.Document(
                    {
                        'name': name,
                        'ticket_id': ticket_id,
                        'uuid': uuid,
                        'blob_link': blob_link,
                        'id': id
                    }
                )
            ]
        )

        
        # Act
        response = main(request, attachments)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json[0]['name'] == name
        assert response_json[0]['ticket_id'] == ticket_id
        assert response_json[0]['uuid'] == uuid
        assert response_json[0]['blob_link'] == blob_link
        assert response_json[0]['id'] == id


    def test_get_attachments_no_attachments(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachments',
            params={
                'ticket_id': ticket_id
            },
            body=None
        )

        attachments = None
      
        # Act
        response = main(request, attachments)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert f'Could not find any attachment for a ticket with ID {ticket_id}.' in response.get_body().decode()


    def test_get_attachments_no_ticketid(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachments',
            params={},
            body=None
        )

        attachments = None

        # Act
        response = main(request, attachments)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please provide a ticket ID to query for.' in response.get_body().decode()