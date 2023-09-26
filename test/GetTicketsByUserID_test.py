import unittest
import azure.functions as func
import json
import datetime

from GetTicketsByUserID import main # import the method we want to test


ticket_id_1 = '4536njnf-389dsf2-fds7f9sd-43u8hdslafsdkfu'
author_id_1 = 'fds7f9sd-43u8hdslafsdkfu-4536njnf-389dsf2'
course_id_1 = 'fds7f9sd-4536njnf-43u8hdslafsdkfu-4536njnf'
document_id_1 = '43u8hdslafsdkfu-4536njnf-fds7f9sd-4536njnf'
ticket_type_1 = 'issue'
description_1 = 'This is my ticket!'
status_1 = 'new'
createdAt_1 = datetime.datetime.utcnow().isoformat()

ticket_id_2 = '4536njnf-323sdfa-fds7f9sd-43u8fdfhdslafsdkfu'
author_id_2 = 'fdsdd7f9sd-43u8hdslaffadsdkfu-fda-fa3r3'
course_id_2 = 'fds7fdd9sd-453dd6njnf-43u8hdsladdfsdkfu-4536njnf'
document_id_2 = '43u8lafsdfdskfu-4536njdnf-fds7df9sd-4536njnfd'
ticket_type_2 = 'question'
description_2 = 'This is my second ticket!'
status_2 = 'in_progress'
createdAt_2 = datetime.datetime.utcnow().isoformat()


class TestGetTicketsByUserID(unittest.TestCase):
    def test_get_ticket_by_user_id_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetTicketsByUserID',
            params={"user_id": "test@test.com"},
            body=None
        )

        tickets = func.DocumentList(
            [
                func.Document(
                    {
                        'id': ticket_id_1,
                        'author_id': author_id_1,
                        'course_id': course_id_1,
                        'document_id': document_id_1,
                        'ticket_type': ticket_type_1,
                        'description': description_1,
                        'status': status_1,
                        'createdAt': createdAt_1
                    }
                ),
                func.Document(
                    {
                        'id': ticket_id_2,
                        'author_id': author_id_2,
                        'course_id': course_id_2,
                        'document_id': document_id_2,
                        'ticket_type': ticket_type_2,
                        'description': description_2,
                        'status': status_2,
                        'createdAt': createdAt_2
                    }
                )
            ]
        )

        # Act
        response = main(request, tickets)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json[0]['id'] == ticket_id_1
        assert response_json[0]['author_id'] == author_id_1
        assert response_json[0]['course_id'] == course_id_1
        assert response_json[0]['document_id'] == document_id_1
        assert response_json[0]['ticket_type'] == ticket_type_1
        assert response_json[0]['description'] == description_1
        assert response_json[0]['status'] == status_1
        assert response_json[0]['createdAt'] == createdAt_1

        assert response_json[1]['id'] == ticket_id_2
        assert response_json[1]['author_id'] == author_id_2
        assert response_json[1]['course_id'] == course_id_2
        assert response_json[1]['document_id'] == document_id_2
        assert response_json[1]['ticket_type'] == ticket_type_2
        assert response_json[1]['description'] == description_2
        assert response_json[1]['status'] == status_2
        assert response_json[1]['createdAt'] == createdAt_2

    
    def test_get_ticket_by_user_id_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetTicketsByUserID',
            params={},
            body=None
        )

        tickets = func.DocumentList(initlist=None)

        # Act
        response = main(request, tickets)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please provide a user ID.' in response.get_body().decode()