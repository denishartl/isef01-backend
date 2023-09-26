import azure.functions as func
import json
import logging
import requests

"""

Returns a list of tickets based on the user ID provided.
If user is role "Bearbeiter", return all tickets.
If user is role "User", only return user's own tickets

"""

def main(req: func.HttpRequest, usertickets: func.DocumentList, alltickets: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    user_id = req.params.get('user_id')
    if not user_id:
        return func.HttpResponse(
            "Please provide a user ID.",
            status_code=400
        )

    user_response = requests.get(f'https://iu-isef01-functionapp.azurewebsites.net/api/getuser?user_id={user_id}')
    user_response_json = json.loads(user_response.content)

    if user_response_json['role'] == 'Bearbeiter':
        tickets_to_return = alltickets
    elif user_response_json['role'] == 'User':
         tickets_to_return = usertickets

    try:
            # Returns a list of all tickets
                ticket_list = []
                for ticket in tickets_to_return:
                    ticket_data = {
                        'id': ticket ['id'],
                        'author_id': ticket ['author_id'],
                        'course_id': ticket ['course_id'],
                        'document_id': ticket ['document_id'],
                        'ticket_type': ticket ['ticket_type'],
                        'description': ticket ['description'],
                        'status': ticket ['status'],
                        'createdAt': ticket ['createdAt']
                }
                    ticket_list.append(ticket_data)

                return func.HttpResponse(
                    json.dumps(ticket_list),
                    status_code=200
                )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error ticket data could not be issued.",
            status_code=500
                )

