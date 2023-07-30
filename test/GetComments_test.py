import unittest
import azure.functions as func
import json

from GetComments import main # import the method we want to test

ticket_id = 'testing_id_do_not_delete'
author_id = '26fd56asf'
text1 = 'Mein erster Kommentar!'
text2 = 'Mein zweiter Kommentar!'
createdAt = '2023-07-19T18:56:50.283239'
id1 = 'a34db788-b1df-4b0b-b893-468a6c000299'
id2 = 'a3ghb788-4gdf-j6fb-8d6s-28fdsa8asf45'
    

class TestGetComments(unittest.TestCase):
    def test_get_comments_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetComments',
            params={
                'ticket_id': ticket_id
            },
            body=None
        )

        comments = func.DocumentList(
            [
                func.Document(
                    {
                        'ticket': ticket_id,
                        'author': author_id,
                        'text': text1,
                        'createdAt': createdAt,
                        'id': id1
                    }
                ),
                func.Document(
                    {
                        'ticket': ticket_id,
                        'author': author_id,
                        'text': text2,
                        'createdAt': createdAt,
                        'id': id2
                    }
                ),
            ]
        )
        
        # Act
        response = main(request, comments)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json[0]['ticket'] == ticket_id
        assert response_json[0]['author'] == author_id
        assert response_json[0]['text'] == text1
        assert response_json[0]['createdAt'] == createdAt
        assert response_json[0]['id'] == id1

        assert response_json[1]['ticket'] == ticket_id
        assert response_json[1]['author'] == author_id
        assert response_json[1]['text'] == text2
        assert response_json[1]['createdAt'] == createdAt
        assert response_json[1]['id'] == id2


    def test_get_comments_no_attachments(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetComments',
            params={
                'ticket_id': ticket_id
            },
            body=None
        )

        comments = None
      
        # Act
        response = main(request, comments)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert f'Could not find any comment for a ticket with ID {ticket_id}.' in response.get_body().decode()


    def test_get_comments_no_ticketid(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetComments',
            params={},
            body=None
        )

        comments = None

        # Act
        response = main(request, comments)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please provide a ticket ID to query for.' in response.get_body().decode()