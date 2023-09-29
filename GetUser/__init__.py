import azure.functions as func
import json
import logging

"""
Gets and returns a user out of Azure CosmosDB

Expected query parameters:
* user_id: ID of the user to retunr
"""


def main(req: func.HttpRequest, user: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')
    if not user_id:
        return func.HttpResponse(
            "Please provide a user_id parameter.",
            status_code=400
        )

    if not user:
        return func.HttpResponse(
            f"Could not find user with the ID {user_id}.",
            status_code=400
        )

    else:
        try:
            # Get ticket from CosmosDB via ticket_id
            user_doc = {
                'id': user[0]['id'],
                'password': user[0]['password'],
                'surname': user[0]['surname'],
                'lastname': user[0]['lastname'],
                'role': user[0]['role']
            }

            # Returns the ticket data as http response
            return func.HttpResponse(
                json.dumps(user_doc),
                status_code=200
            )

        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                "Error finding user",
                status_code=500
            )
