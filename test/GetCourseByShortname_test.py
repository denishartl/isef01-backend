import unittest
import azure.functions as func
import json

from GetCourseByShortname import main # import the method we want to test


course_id = '52556c2c-28bb-11ee-a541-4ead18658f42'
course_shortname = 'ISEF01'
course_name = 'Projekt Software Engineering'


class TestGetCourseByShortname(unittest.TestCase):
    def test_get_course_by_shortname_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetCourseByShortname',
            params={'shortname': course_shortname},
            body=None
        )

        course = func.DocumentList(
            [
                func.Document(
                    {
                        'id': course_id,
                        'shortname': course_shortname,
                        'name': course_name
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
        assert response_json['id'] == course_id
        assert response_json['shortname'] == course_shortname
        assert response_json['name'] == course_name


    def test_get_course_by_shortname_noparam(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetCourseByShortname',
            params={},
            body=None
        )

        document = func.DocumentList(initlist=None)

        # Act
        response = main(request,document)

        # Assert status code
        assert response.status_code == 400

        # Assert the response is as expected
        assert 'Please insert course shortname.' in response.get_body().decode()

    def test_get_course_by_shortname_unknowncourse(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetCourseByShortame',
            params={'shortname': course_shortname},
            body=None
        )

        course = func.DocumentList(initlist=None)

        # Act
        response = main(request,course)

        # Assert status code
        assert response.status_code == 404

        # Assert the response is as expected
        assert f'Could not find a course with the shortname {course_shortname}.' in response.get_body().decode()
