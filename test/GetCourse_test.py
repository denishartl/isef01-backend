import unittest
import azure.functions as func
import json

from GetCourse import main # import the method we want to test

course_id = '32214-fg342-fds856fasd-4fdsaf5sa'
course_shortname = 'ISEF01'
course_name = 'Projekt Software Engineering'
course_id_invalid = 'invalid_course'


class TestGetCourse(unittest.TestCase):
    def test_get_course_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachment',
            params={'id': 'ede37445-7aaf-4df3-802c-f590720f7626'},
            body=None
        )

        course = func.DocumentList(
            [
                func.Document(
                    {
                        'name': course_name,
                        'shortname': course_shortname,
                        'id': course_id
                    }
                )
            ]
        )

        # Act
        response = main(request, course)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the response is as expected
        response_json = json.loads(response.get_body())
        assert response_json['name'] == course_name
        assert response_json['shortname'] == course_shortname
        assert response_json['id'] == course_id


    def test_get_course_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetCourse',
            params={},
            body=None
        )

        course = func.DocumentList(initlist=None)

        # Act
        response = main(request,course)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please insert course ID.' in response.get_body().decode()


    def test_get_course_unknowncourse(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetAttachment',
            params={'id': course_id_invalid},
            body=None
        )

        course = func.DocumentList(initlist=None)

        # Act
        response = main(request,course)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert f'Could not find a course with the ID {course_id_invalid}.' in response.get_body().decode()
