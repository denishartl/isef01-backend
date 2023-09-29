import azure.functions as func
import json
import logging
import requests

"""
Returns a list of users based on the role provided (without password).
"""


def main(req: func.HttpRequest, users: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    role = req.params.get('role')
    if not role:
        return func.HttpResponse(
            "Please provide a role to query for.",
            status_code=400
        )

    if not users:
        return func.HttpResponse(
            "Found no users with this role.",
            status_code=200
        )

    try:
        # Returns a list of all tickets
        user_list = []
        for user in users:
            user_data = {
                'id': user['id'],
                'surname': user['surname'],
                'lastname': user['lastname'],
                'role': user['role']
            }
            user_list.append(user_data)

        return func.HttpResponse(
            json.dumps(user_list),
            status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error fetching user data.",
            status_code=500
        )
