import unittest
import azure.functions as func
import json

from UpdateComment import main # import the method we want to test
from unittest import mock

comment_id = '12331-455ag1-136785-21432'
ticket_id = 'testing_id_do_not_delete'
author_id = '136785-21432-12331-455ag1'
comment_text = 'This is my comment text!'
comment_text_updated = 'This is my edited comment text!'
createdAt = '2023-07-19T18:56:50.283239'
    

class TestUdpateComment(unittest.TestCase):
    def test_update_comment_correct(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateComment',
            params={
                'comment_id': comment_id
            },
            body=json.dumps(
                {
                    'text': comment_text_updated
                }
            ).encode('utf8')
        )

        comment = func.DocumentList(
            [
                func.Document(
                    {
                        'ticket': ticket_id,
                        'author': author_id,
                        'text': comment_text,
                        'createdAt': createdAt,
                        'id': comment_id
                    }
                )
            ]
        )

        outcomment = mock.Mock()
        
        # Act
        response = main(request, comment, outcomment)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outcomment.mock_calls[0][1][0].data['ticket'] == ticket_id
        assert outcomment.mock_calls[0][1][0].data['author'] == author_id
        assert outcomment.mock_calls[0][1][0].data['text'] == comment_text_updated
        assert outcomment.mock_calls[0][1][0].data['id'] == comment_id
        assert outcomment.mock_calls[0][1][0].data['createdAt'] == createdAt


    def test_update_comment_nobody(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateComment',
            params={
                'comment_id': comment_id
            },
            body=None
        )

        comment = func.DocumentList(initlist=None)
        outcomment = mock.Mock()
        
        # Act
        response = main(request, comment, outcomment)

        # Assert
        # Assert status code
        assert response.status_code == 500


    def test_update_comment_nocommentid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateComment',
            params={},
            body=json.dumps(
                {
                    'text': comment_text_updated
                }
            ).encode('utf8')
        )

        comment = func.DocumentList(initlist=None)
        outcomment = mock.Mock()
        
        # Act
        response = main(request, comment, outcomment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'Please provide a comment ID to query for.' in response.get_body().decode()


    def test_update_comment_notext(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateComment',
            params={
                'comment_id': comment_id
            },
            body=json.dumps(
                {
                }
            ).encode('utf8')
        )

        comment = func.DocumentList(
            [
                func.Document(
                    {
                        'ticket': ticket_id,
                        'author': author_id,
                        'text': comment_text,
                        'createdAt': createdAt,
                        'id': comment_id
                    }
                )
            ]
        )
        outcomment = mock.Mock()
        
        # Act
        response = main(request, comment, outcomment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'No text provided. Please pass a text in the body when calling this function.' in response.get_body().decode()


    def test_update_comment_invalidcommentid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateComment',
            params={
                'comment_id': comment_id
            },
            body=json.dumps(
                {
                    'text': comment_text_updated
                }
            ).encode('utf8')
        )

        comment = func.DocumentList(initlist=None)
        outcomment = mock.Mock()
        
        # Act
        response = main(request, comment, outcomment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert f"Could not find any comment with ID {comment_id}." in response.get_body().decode()
