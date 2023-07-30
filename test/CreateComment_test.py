import unittest
import azure.functions as func
import json

from CreateComment import main # import the method we want to test
from unittest import mock

ticket_id = 'testing_id_do_not_delete'
author_id = '136785-21432-12331-455ag1'
comment_text = 'This is my comment text!'
    

class TestCreateComment(unittest.TestCase):
    def test_create_attachment_correct(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateComment',
            params={},
            body=json.dumps(
                {
                    'ticket_id': ticket_id,
                    'author_id': author_id,
                    'text': comment_text
                }
            ).encode('utf8')
        )

        comment = mock.Mock()
        
        # Act
        response = main(request, comment)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert comment.mock_calls[0][1][0].data['ticket'] == ticket_id
        assert comment.mock_calls[0][1][0].data['author'] == author_id
        assert comment.mock_calls[0][1][0].data['text'] == comment_text


    def test_create_attachment_nobody(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateComment',
            params={},
            body=json.dumps('').encode('utf8')
        )

        comment = mock.Mock()
        
        # Act
        response = main(request, comment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'Body is not in JSON format. Please provide a valid JSON formated body.' in response.get_body().decode()


    def test_create_attachment_noticketid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateComment',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'text': comment_text
                }
            ).encode('utf8')
        )

        comment = mock.Mock()
        
        # Act
        response = main(request, comment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'No ticket ID provided. Please pass a ticket ID in the body when calling this function.' in response.get_body().decode()

    def test_create_attachment_noauthorid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateComment',
            params={},
            body=json.dumps(
                {
                    'ticket_id': ticket_id,
                    'text': comment_text
                }
            ).encode('utf8')
        )

        comment = mock.Mock()
        
        # Act
        response = main(request, comment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'No author ID provided. Please pass a author ID in the body when calling this function.' in response.get_body().decode()


    def test_create_attachment_notext(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateComment',
            params={},
            body=json.dumps(
                {
                    'ticket_id': ticket_id,
                    'author_id': author_id
                }
            ).encode('utf8')
        )

        comment = mock.Mock()
        
        # Act
        response = main(request, comment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'No text provided. Please pass a text in the body when calling this function.' in response.get_body().decode()
