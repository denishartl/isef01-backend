import unittest
import azure.functions as func
import json

from CreateTicket import main # import the method we want to test
from unittest import mock

author_id = '45345-543dsds-543543fds-fdsf7af90asf'
course_id = '543543fds-fdsf7af90asf-45345-543dsds'
document_id = '45345-543dsds-45345-543dsds'
ticket_type = 'issue'
description = 'My ticket description!'  
assignee = '3fds-fdsf7af90asf-4534' 


class TestCreateTicket(unittest.TestCase):
    def test_create_ticket_correct(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'course_id': course_id,
                    'document_id': document_id,
                    'ticket_type': ticket_type,
                    'description': description,
                    'assignee': assignee
                }
            ).encode('utf8')
        )

        ticket = mock.Mock()
        
        # Act
        response = main(request, ticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert ticket.mock_calls[0][1][0].data['author_id'] == author_id
        assert ticket.mock_calls[0][1][0].data['course_id'] == course_id
        assert ticket.mock_calls[0][1][0].data['document_id'] == document_id
        assert ticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type
        assert ticket.mock_calls[0][1][0].data['description'] == description
        assert ticket.mock_calls[0][1][0].data['status'] == 'Neu'
        assert ticket.mock_calls[0][1][0].data['assignee'] == assignee


    def test_create_ticket_nobody(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=None
        )

        ticket = mock.Mock()
        
        # Act
        response = main(request, ticket)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'No body provided. Please provide a JSON body.' in response.get_body().decode()


    def test_create_ticket_noauthorid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'course_id': course_id,
                    'document_id': document_id,
                    'ticket_type': ticket_type,
                    'description': description,
                    'assignee': assignee
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
        assert 'Missing required parameters.' in response.get_body().decode()

    
    def test_create_ticket_nocourseid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'document_id': document_id,
                    'ticket_type': ticket_type,
                    'description': description,
                    'assignee': assignee
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
        assert 'Missing required parameters.' in response.get_body().decode()


    def test_create_ticket_nodocumentid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'course_id': course_id,
                    'ticket_type': ticket_type,
                    'description': description,
                    'assignee': assignee
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
        assert 'Missing required parameters.' in response.get_body().decode()


    def test_create_ticket_notickettype(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'course_id': course_id,
                    'document_id': document_id,
                    'description': description,
                    'assignee': assignee
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
        assert 'Missing required parameters.' in response.get_body().decode()


    def test_create_ticket_nodescription(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'course_id': course_id,
                    'document_id': document_id,
                    'ticket_type': ticket_type,
                    'assignee': assignee
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
        assert 'Missing required parameters.' in response.get_body().decode()


    def test_create_ticket_noassignee(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/CreateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id,
                    'course_id': course_id,
                    'document_id': document_id,
                    'ticket_type': ticket_type,
                    'description': description
                }
            ).encode('utf8')
        )

        ticket = mock.Mock()
        
        # Act
        response = main(request, ticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert request response
        assert ticket.mock_calls[0][1][0].data['author_id'] == author_id
        assert ticket.mock_calls[0][1][0].data['course_id'] == course_id
        assert ticket.mock_calls[0][1][0].data['document_id'] == document_id
        assert ticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type
        assert ticket.mock_calls[0][1][0].data['description'] == description
        assert ticket.mock_calls[0][1][0].data['status'] == 'Neu'
        assert ticket.mock_calls[0][1][0].data['assignee'] == None