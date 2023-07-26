import base64
import unittest
import azure.functions as func
import json
import requests

from CreateAttachment import main # import the method we want to test
from unittest import mock

filename = 'testfile.png'
ticket_id = 'testing_id_do_not_delete'
file = 'PG14ZmlsZSBob3N0PSJFbGVjdHJvbiIgbW9kaWZpZWQ9IjIwMjMtMDYtMjRUMTI6NDY6NTcuNjQ4WiIgYWdlbnQ9Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRyYXcuaW8vMjEuMi44IENocm9tZS8xMTIuMC41NjE1LjE2NSBFbGVjdHJvbi8yNC4yLjAgU2FmYXJpLzUzNy4zNiIgZXRhZz0iOGJHZ2VHRk9lODlCUkRlci1DSlAiIHZlcnNpb249IjIxLjIuOCIgdHlwZT0iZGV2aWNlIj4KICA8ZGlhZ3JhbSBuYW1lPSJQYWdlLTEiIGlkPSJwbUFoTXo4OEVBRFMxYVphd2oxayI+CiAgICA8bXhHcmFwaE1vZGVsIGR4PSI4OTEiIGR5PSIxMTczIiBncmlkPSIxIiBncmlkU2l6ZT0iMTAiIGd1aWRlcz0iMSIgdG9vbHRpcHM9IjEiIGNvbm5lY3Q9IjEiIGFycm93cz0iMSIgZm9sZD0iMSIgcGFnZT0iMSIgcGFnZVNjYWxlPSIxIiBwYWdlV2lkdGg9IjgyNyIgcGFnZUhlaWdodD0iMTE2OSIgbWF0aD0iMCIgc2hhZG93PSIwIj4KICAgICAgPHJvb3Q+CiAgICAgICAgPG14Q2VsbCBpZD0iMCIgLz4KICAgICAgICA8bXhDZWxsIGlkPSIxIiBwYXJlbnQ9IjAiIC8+CiAgICAgICAgPG14Q2VsbCBpZD0icFhQLTNOMlVZODJSNEEwNkpaMjctNiIgc3R5bGU9ImVkZ2VTdHlsZT1vcnRob2dvbmFsRWRnZVN0eWxlO3JvdW5kZWQ9MDtvcnRob2dvbmFsTG9vcD0xO2pldHR5U2l6ZT1hdXRvO2h0bWw9MTsiIGVkZ2U9IjEiIHBhcmVudD0iMSIgc291cmNlPSJwWFAtM04yVVk4MlI0QTA2SloyNy0xIiB0YXJnZXQ9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTIiPgogICAgICAgICAgPG14R2VvbWV0cnkgcmVsYXRpdmU9IjEiIGFzPSJnZW9tZXRyeSIgLz4KICAgICAgICA8L214Q2VsbD4KICAgICAgICA8bXhDZWxsIGlkPSJwWFAtM04yVVk4MlI0QTA2SloyNy03IiBzdHlsZT0iZWRnZVN0eWxlPW9ydGhvZ29uYWxFZGdlU3R5bGU7cm91bmRlZD0wO29ydGhvZ29uYWxMb29wPTE7amV0dHlTaXplPWF1dG87aHRtbD0xOyIgZWRnZT0iMSIgcGFyZW50PSIxIiBzb3VyY2U9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTEiIHRhcmdldD0icFhQLTNOMlVZODJSNEEwNkpaMjctMyI+CiAgICAgICAgICA8bXhHZW9tZXRyeSByZWxhdGl2ZT0iMSIgYXM9Imdlb21ldHJ5IiAvPgogICAgICAgIDwvbXhDZWxsPgogICAgICAgIDxteENlbGwgaWQ9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTEiIHZhbHVlPSJOZXVlIERhdGVuIiBzdHlsZT0icm91bmRlZD0wO3doaXRlU3BhY2U9d3JhcDtodG1sPTE7IiB2ZXJ0ZXg9IjEiIHBhcmVudD0iMSI+CiAgICAgICAgICA8bXhHZW9tZXRyeSB4PSIxODAiIHk9IjIzMCIgd2lkdGg9IjEyMCIgaGVpZ2h0PSI2MCIgYXM9Imdlb21ldHJ5IiAvPgogICAgICAgIDwvbXhDZWxsPgogICAgICAgIDxteENlbGwgaWQ9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTgiIHN0eWxlPSJlZGdlU3R5bGU9b3J0aG9nb25hbEVkZ2VTdHlsZTtyb3VuZGVkPTA7b3J0aG9nb25hbExvb3A9MTtqZXR0eVNpemU9YXV0bztodG1sPTE7IiBlZGdlPSIxIiBwYXJlbnQ9IjEiIHNvdXJjZT0icFhQLTNOMlVZODJSNEEwNkpaMjctMiIgdGFyZ2V0PSJwWFAtM04yVVk4MlI0QTA2SloyNy00Ij4KICAgICAgICAgIDxteEdlb21ldHJ5IHJlbGF0aXZlPSIxIiBhcz0iZ2VvbWV0cnkiIC8+CiAgICAgICAgPC9teENlbGw+CiAgICAgICAgPG14Q2VsbCBpZD0icFhQLTNOMlVZODJSNEEwNkpaMjctMiIgdmFsdWU9IkJhdGNoIExheWVyIiBzdHlsZT0icm91bmRlZD0wO3doaXRlU3BhY2U9d3JhcDtodG1sPTE7IiB2ZXJ0ZXg9IjEiIHBhcmVudD0iMSI+CiAgICAgICAgICA8bXhHZW9tZXRyeSB4PSIzNTAiIHk9IjE4MCIgd2lkdGg9IjEyMCIgaGVpZ2h0PSI2MCIgYXM9Imdlb21ldHJ5IiAvPgogICAgICAgIDwvbXhDZWxsPgogICAgICAgIDxteENlbGwgaWQ9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTEwIiBzdHlsZT0iZWRnZVN0eWxlPW9ydGhvZ29uYWxFZGdlU3R5bGU7cm91bmRlZD0wO29ydGhvZ29uYWxMb29wPTE7amV0dHlTaXplPWF1dG87aHRtbD0xOyIgZWRnZT0iMSIgcGFyZW50PSIxIiBzb3VyY2U9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTMiIHRhcmdldD0icFhQLTNOMlVZODJSNEEwNkpaMjctNSI+CiAgICAgICAgICA8bXhHZW9tZXRyeSByZWxhdGl2ZT0iMSIgYXM9Imdlb21ldHJ5Ij4KICAgICAgICAgICAgPEFycmF5IGFzPSJwb2ludHMiPgogICAgICAgICAgICAgIDxteFBvaW50IHg9IjY2MCIgeT0iMzEwIiAvPgogICAgICAgICAgICAgIDxteFBvaW50IHg9IjY2MCIgeT0iMjYwIiAvPgogICAgICAgICAgICA8L0FycmF5PgogICAgICAgICAgPC9teEdlb21ldHJ5PgogICAgICAgIDwvbXhDZWxsPgogICAgICAgIDxteENlbGwgaWQ9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTMiIHZhbHVlPSJTcGVlZCBMYXllciIgc3R5bGU9InJvdW5kZWQ9MDt3aGl0ZVNwYWNlPXdyYXA7aHRtbD0xO2FsaWduPWNlbnRlcjsiIHZlcnRleD0iMSIgcGFyZW50PSIxIj4KICAgICAgICAgIDxteEdlb21ldHJ5IHg9IjM1MCIgeT0iMjcwIiB3aWR0aD0iMTIwIiBoZWlnaHQ9IjgwIiBhcz0iZ2VvbWV0cnkiIC8+CiAgICAgICAgPC9teENlbGw+CiAgICAgICAgPG14Q2VsbCBpZD0icFhQLTNOMlVZODJSNEEwNkpaMjctOSIgc3R5bGU9ImVkZ2VTdHlsZT1vcnRob2dvbmFsRWRnZVN0eWxlO3JvdW5kZWQ9MDtvcnRob2dvbmFsTG9vcD0xO2pldHR5U2l6ZT1hdXRvO2h0bWw9MTsiIGVkZ2U9IjEiIHBhcmVudD0iMSIgc291cmNlPSJwWFAtM04yVVk4MlI0QTA2SloyNy00IiB0YXJnZXQ9InBYUC0zTjJVWTgyUjRBMDZKWjI3LTUiPgogICAgICAgICAgPG14R2VvbWV0cnkgcmVsYXRpdmU9IjEiIGFzPSJnZW9tZXRyeSI+CiAgICAgICAgICAgIDxBcnJheSBhcz0icG9pbnRzIj4KICAgICAgICAgICAgICA8bXhQb2ludCB4PSI2NjAiIHk9IjIxMCIgLz4KICAgICAgICAgICAgICA8bXhQb2ludCB4PSI2NjAiIHk9IjI2MCIgLz4KICAgICAgICAgICAgPC9BcnJheT4KICAgICAgICAgIDwvbXhHZW9tZXRyeT4KICAgICAgICA8L214Q2VsbD4KICAgICAgICA8bXhDZWxsIGlkPSJwWFAtM04yVVk4MlI0QTA2SloyNy00IiB2YWx1ZT0iU2VydmluZyBMYXllciIgc3R5bGU9InJvdW5kZWQ9MDt3aGl0ZVNwYWNlPXdyYXA7aHRtbD0xOyIgdmVydGV4PSIxIiBwYXJlbnQ9IjEiPgogICAgICAgICAgPG14R2VvbWV0cnkgeD0iNTIwIiB5PSIxNzAiIHdpZHRoPSIxMjAiIGhlaWdodD0iODAiIGFzPSJnZW9tZXRyeSIgLz4KICAgICAgICA8L214Q2VsbD4KICAgICAgICA8bXhDZWxsIGlkPSJwWFAtM04yVVk4MlI0QTA2SloyNy01IiB2YWx1ZT0iQWJmcmFnZW4iIHN0eWxlPSJyb3VuZGVkPTA7d2hpdGVTcGFjZT13cmFwO2h0bWw9MTsiIHZlcnRleD0iMSIgcGFyZW50PSIxIj4KICAgICAgICAgIDxteEdlb21ldHJ5IHg9IjY5MCIgeT0iMjMwIiB3aWR0aD0iMTIwIiBoZWlnaHQ9IjYwIiBhcz0iZ2VvbWV0cnkiIC8+CiAgICAgICAgPC9teENlbGw+CiAgICAgICAgPG14Q2VsbCBpZD0icFhQLTNOMlVZODJSNEEwNkpaMjctMTEiIHZhbHVlPSJFY2h0emVpdC1WaWV3cyIgc3R5bGU9InJvdW5kZWQ9MDt3aGl0ZVNwYWNlPXdyYXA7aHRtbD0xO2ZpbGxDb2xvcj0jZmZmMmNjO3N0cm9rZUNvbG9yPSNkNmI2NTY7IiB2ZXJ0ZXg9IjEiIHBhcmVudD0iMSI+CiAgICAgICAgICA8bXhHZW9tZXRyeSB4PSI0MDAiIHk9IjMzMCIgd2lkdGg9IjkwIiBoZWlnaHQ9IjMwIiBhcz0iZ2VvbWV0cnkiIC8+CiAgICAgICAgPC9teENlbGw+CiAgICAgICAgPG14Q2VsbCBpZD0icFhQLTNOMlVZODJSNEEwNkpaMjctMTIiIHZhbHVlPSJCYXRjaC1WaWV3cyIgc3R5bGU9InJvdW5kZWQ9MDt3aGl0ZVNwYWNlPXdyYXA7aHRtbD0xO2ZpbGxDb2xvcj0jZGFlOGZjO3N0cm9rZUNvbG9yPSM2YzhlYmY7IiB2ZXJ0ZXg9IjEiIHBhcmVudD0iMSI+CiAgICAgICAgICA8bXhHZW9tZXRyeSB4PSI1NjAiIHk9IjIzMCIgd2lkdGg9IjkwIiBoZWlnaHQ9IjMwIiBhcz0iZ2VvbWV0cnkiIC8+CiAgICAgICAgPC9teENlbGw+CiAgICAgIDwvcm9vdD4KICAgIDwvbXhHcmFwaE1vZGVsPgogIDwvZGlhZ3JhbT4KPC9teGZpbGU+Cg=='
    

class TestCreateAttachment(unittest.TestCase):
    def test_create_attachment_correct(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/GetCreateAttachment',
            params={
                'name': filename,
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'file': file
                }
            ).encode('utf8')
        )

        attachment = mock.Mock()
        
        # Act
        response = main(request, attachment)

        # Assert
        # Assert status code
        assert response.status_code == 200

        # Assert the CosmosDB output binding is working correctly
        assert attachment.mock_calls[0][1][0].data['name'] == filename
        assert attachment.mock_calls[0][1][0].data['ticket_id'] == ticket_id

        # Assert the file content is correct
        downloaded_blob = requests.get(attachment.mock_calls[0][1][0].data['blob_link'], allow_redirects=True)
        assert (base64.b64encode(downloaded_blob.content)).decode() == file


    def test_create_attachment_noparam(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/GetCreateAttachment',
            params={},
            body=json.dumps(
                {
                    'file': file
                }
            ).encode('utf8')
        )

        attachment = mock.Mock()

        # Act
        response = main(request, attachment)

        # Assert
        # Assert status code
        assert response.status_code == 400


    def test_create_attachment_noname(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/GetCreateAttachment',
            params={
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                    'file': file
                }
            ).encode('utf8')
        )

        attachment = mock.Mock()

        # Act
        response = main(request, attachment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'Please provide a name as a query parameter.' in response.get_body().decode()

    def test_create_attachment_noticketid(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/GetCreateAttachment',
            params={
                'name': filename
            },
            body=json.dumps(
                {
                    'file': file
                }
            ).encode('utf8')
        )

        attachment = mock.Mock()

        # Act
        response = main(request, attachment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'Please provide a ticket_id as a query parameter.' in response.get_body().decode()

    def test_create_attachment_nofile(self):
        request = func.HttpRequest(
            method='POST',
            url='/api/GetCreateAttachment',
            params={
                'name': filename,
                'ticket_id': ticket_id
            },
            body=json.dumps(
                {
                }
            ).encode('utf8')
        )

        attachment = mock.Mock()

        # Act
        response = main(request, attachment)

        # Assert
        # Assert status code
        assert response.status_code == 400

        # Assert request response
        assert 'No file provided. Please pass a file in base64 encoded format in the body when calling this function.' in response.get_body().decode()

        



        # wrong ticketid (Check for that still needs to be implemented)