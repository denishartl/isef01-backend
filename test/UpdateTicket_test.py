import unittest
import azure.functions as func
import json

from UpdateTicket import main # import the method we want to test
from unittest import mock

ticket_id = '45345-543dsds-543543fds-fdsf7af90asf-45345'
author_id = '45345-543dsds-543543fds-fdsf7af90asf'
author_id_updated = '45345-543dsds-543543fds-fdsf7af90asg'
course_id = '543543fds-fdsf7af90asf-45345-543dsds'
course_id_updated = '543543fds-fdsf7af90asf-45345-543dsdg'
document_id = '45345-543dsds-45345-543dsds'
document_id_updated = '45345-543dsds-45345-543dsdg'
ticket_type = 'issue'
ticket_type_updated = 'question'
description = 'My ticket description!' 
description_updated = 'My updated ticket description!' 
status = 'in_progress'
status_updated = 'waiting'
status_closed = 'closed'
    

class TestUdpateTicket(unittest.TestCase):
    def test_update_ticket_correct(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status_updated


    def test_update_ticket_correct_close(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_closed
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status_closed
        assert outticket.mock_calls[0][1][0].data['resolvedAt'] != None


    def test_update_ticket_noparam(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={},
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_updated
                }
            ).encode('utf8')
        )

        ticket = func.DocumentList(initlist=None)

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert the response
        assert f"Please provide a Ticket ID to query for." in response.get_body().decode()


    def test_update_ticket_nobody(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 500


    def test_update_ticket_wrongparam(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_closed
                }
            ).encode('utf8')
        )

        ticket = func.DocumentList(initlist=None)

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 404

        # Assert the CosmosDB output binding is working correctly
        assert f"Ticket not found" in response.get_body().decode()


    def test_update_ticket_missingauthorid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status_updated


    def test_update_ticket_missingcourseid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status_updated


    def test_update_ticket_missingdocumentid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated,
                    'status': status_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status_updated


    def test_update_ticket_missingtickettype(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'description': description_updated,
                    'status': status_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status_updated


    def test_update_ticket_missingdescription(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'status': status_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description
        assert outticket.mock_calls[0][1][0].data['status'] == status_updated


    def test_update_ticket_missingstatus(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/UpdateTicket',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'author_id': author_id_updated,
                    'course_id': course_id_updated,
                    'document_id': document_id_updated,
                    'ticket_type': ticket_type_updated,
                    'description': description_updated
                }
            ).encode('utf8')
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
                        'status': status
                    }
                )
            ]
        )

        outticket = mock.Mock()
        
        # Act
        response = main(request, ticket, outticket)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert outticket.mock_calls[0][1][0].data['id'] == ticket_id
        assert outticket.mock_calls[0][1][0].data['author_id'] == author_id_updated
        assert outticket.mock_calls[0][1][0].data['course_id'] == course_id_updated
        assert outticket.mock_calls[0][1][0].data['document_id'] == document_id_updated
        assert outticket.mock_calls[0][1][0].data['ticket_type'] == ticket_type_updated
        assert outticket.mock_calls[0][1][0].data['description'] == description_updated
        assert outticket.mock_calls[0][1][0].data['status'] == status