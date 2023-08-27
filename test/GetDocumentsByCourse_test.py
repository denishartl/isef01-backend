import unittest
import azure.functions as func
import json

from GetDocumentsByCourse import main # import the method we want to test

course_id = '52556c2c-28bb-11ee-a541-4ead18658f42'
document_id_1 = '32214-fg342-fds856fasd-4fdsaf5sa'
document_title_1 = 'ISSE01 - Skript'
document_doctype_1 = 'Skript'
document_id_2 = 'fasd5-kjh15-1281kjhg6g-4jfhg83d1'
document_title_2 = 'ISSE01 - Live Session 1 Aufzeichnung'
document_doctype_2 = 'Video'
    

class TestGetDocumentsByCourse(unittest.TestCase):
    def test_get_documents_by_course_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetDocumentsByCourse',
            params={'course': course_id},
            body=None
        )

        documents = func.DocumentList(
            [
                func.Document(
                    {
                        'id': document_id_1,
                        'title': document_title_1,
                        'doctype': document_doctype_1,
                        'course': course_id
                    }
                ),
                func.Document(
                    {
                        'id': document_id_2,
                        'title': document_title_2,
                        'doctype': document_doctype_2,
                        'course': course_id
                    }
                ),
            ]
        )
        
        # Act
        response = main(request, documents)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json[0]['id'] == document_id_1
        assert response_json[0]['title'] == document_title_1
        assert response_json[0]['doctype'] == document_doctype_1
        assert response_json[0]['course'] == course_id

        assert response_json[1]['id'] == document_id_2
        assert response_json[1]['title'] == document_title_2
        assert response_json[1]['doctype'] == document_doctype_2
        assert response_json[1]['course'] == course_id

    
    def test_get_documents_by_course_id_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetDocumentsByCourse',
            params={},
            body=None
        )

        documents = func.DocumentList(initlist=None)

        # Act
        response = main(request,documents)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please choose a course ID.' in response.get_body().decode()
