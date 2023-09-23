import unittest
import azure.functions as func
import json
import datetime

from GetLatestTicket import main


ticket_id = '4536njnf-389dsf2-fds7f9sd-43u8hdslafsdkfu'
author_id = 'fds7f9sd-43u8hdslafsdkfu-4536njnf-389dsf2'
course_id = 'fds7f9sd-4536njnf-43u8hdslafsdkfu-4536njnf'
document_id = '43u8hdslafsdkfu-4536njnf-fds7f9sd-4536njnf'
ticket_type = 'issue'
description = 'This is my ticket!'
status = 'new'
createdAt = datetime.datetime.utcnow().isoformat()


class TestGetLatestTicket(unittest.TestCase):
    def test_get_latest_ticket_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetLatestTicket',
            params={},
            body=None
        )

        ticket = func.DocumentList(
            [
                func.Document(
                    {
                        'id': ticket_id,
                        'author_id': author_id,
                        'course_id': course_id,
                        'document_id': document_id,
                        'ticket_type': ticket_type,
                        'description': description,
                        'status': status,
                        'createdAt': createdAt
                    }
                )
            ]
        )

        # Act
        response = main(request, ticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json['id'] == ticket_id
        assert response_json['author_id'] == author_id
        assert response_json['course_id'] == course_id
        assert response_json['document_id'] == document_id
        assert response_json['ticket_type'] == ticket_type
        assert response_json['description'] == description
        assert response_json['status'] == status
        assert response_json['createdAt'] == createdAt


    def test_get_ticket_noticket(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetLatestTicket',
            params={},
            body=None
        )

        ticket = func.DocumentList(initlist=None)

        # Act
        response = main(request,ticket)

        # Assert status code
        assert response.status_code == 500

        # Assert the response is as expected
        assert 'Could not fetch latest ticket.' in response.get_body().decode()