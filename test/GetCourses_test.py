import unittest
import azure.functions as func
import json

from GetCourses import main # import the method we want to test

course_id_1 = '32214-fg342-fds856fasd-4fdsaf5sa'
course_shortname_1 = 'ISEF01'
course_name_1 = 'Projekt Software Engineering'
course_id_2 = 'fasd5-kjh15-1281kjhg6g-4jfhg83d1'
course_shortname_2 = 'ISSE01'
course_name_2 = 'Seminar Software Engineering'
    

class TestGetCourses(unittest.TestCase):
    def test_get_courses_correct(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/GetCourses',
            params={},
            body=None
        )

        comments = func.DocumentList(
            [
                func.Document(
                    {
                        'id': course_id_1,
                        'name': course_name_1,
                        'shortname': course_shortname_1
                    }
                ),
                func.Document(
                    {
                        'id': course_id_2,
                        'name': course_name_2,
                        'shortname': course_shortname_2
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
        assert response_json[0]['name'] == course_name_1
        assert response_json[0]['shortname'] == course_shortname_1
        assert response_json[0]['id'] == course_id_1

        assert response_json[1]['name'] == course_name_2
        assert response_json[1]['shortname'] == course_shortname_2
        assert response_json[1]['id'] == course_id_2
