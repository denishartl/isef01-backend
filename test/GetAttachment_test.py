import unittest
import azure.functions as func
import json

from GetAttachment import main # import the method we want to test

name = 'for_testing_do_not_delete.ico'
ticket_id = 69420
uuid = '52556c2c-28bb-11ee-a541-4ead18658f42'
blob_link = 'https://iuisef01b10e.blob.core.windows.net/attachment/52556c2c-28bb-11ee-a541-4ead18658f42'
id = 'ede37445-7aaf-4df3-802c-f590720f7626'
invalid_id = "invalid_id"


class TestGetAttachment(unittest.TestCase):
    def test_get_attachment_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachment',
            params={'id': 'ede37445-7aaf-4df3-802c-f590720f7626'},
            body=None
        )

        attachment = func.DocumentList(
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
        response = main(request, attachment)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json['name'] == name
        assert response_json['ticket_id'] == ticket_id
        assert response_json['uuid'] == uuid
        assert response_json['blob_link'] == blob_link
        assert response_json['id'] == id


    def test_get_attachment_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachment',
            params={},
            body=None
        )

        attachment = func.DocumentList(initlist=None)

        # Act
        response = main(request,attachment)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please provide a attachment ID to query for.' in response.get_body().decode()

    def test_get_attachment_unknownticket(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachment',
            params={'id': invalid_id},
            body=None
        )

        attachment = func.DocumentList(initlist=None)

        # Act
        response = main(request,attachment)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert f'Could not find attachment with ID {invalid_id}.' in response.get_body().decode()
