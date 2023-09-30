import unittest
import azure.functions as func
import json

from GetDocument import main # import the method we want to test

document_id = '32214-fg342-fds856fasd-4fdsaf5sa'
document_title = 'ISEF01 - Skript'
doctype = 'Skript'
course = '2432f-fdswg-3412rdfsd-2esafdd'


class TestGetDocument(unittest.TestCase):
    def test_get_document_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetDocument',
            params={'id': document_id},
            body=None
        )

        document = func.DocumentList(
            [
                func.Document(
                    {
                        'id': document_id,
                        'title': document_title,
                        'doctype': doctype,
                        'course': course
                    }
                )
            ]
        )

        # Act
        response = main(request, document)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json['id'] == document_id
        assert response_json['title'] == document_title
        assert response_json['doctype'] == doctype


    def test_get_document_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetDocument',
            params={},
            body=None
        )

        document = func.DocumentList(initlist=None)

        # Act
        response = main(request,document)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please insert a document ID.' in response.get_body().decode()


    def test_get_document_unknowncourse(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetDocument',
            params={'id': document_id},
            body=None
        )

        document = func.DocumentList(initlist=None)

        # Act
        response = main(request,document)

        # Assert status code
        assert response.status_code == 404

        # Assert the response is as expected
        assert f'Could not find a document with the ID {document_id}.' in response.get_body().decode()
