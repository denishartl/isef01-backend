import datetime
import azure.functions as func
import logging
import requests
import json


def generate_ticket_number():
    datepart = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    latest_ticket = requests.get(
        'https://iu-isef01-functionapp2.azurewebsites.net/api/getlatestticket')
    latest_ticket = json.loads(latest_ticket.content)
    latest_ticket_number = int(latest_ticket['id'][11:])
    new_ticket_number = latest_ticket_number + 1
    new_ticket_id = f"IU-{datepart}{str(new_ticket_number).zfill(8)}"
    return (new_ticket_id)


def main(req: func.HttpRequest,
         ticket: func.Out[func.Document]) -> func.HttpResponse:
    generate_ticket_number()
    logging.info('Python HTTP trigger function processed a request.')

    # Check if JSON Body exists
    try:
        req_body = req.get_json()
        if type(req_body) is str:
            return func.HttpResponse(
                'Body is not in JSON format. Please provide a valid JSON formated body.',
                status_code=400
            )
    except ValueError:
        pass
    except AttributeError:
        return func.HttpResponse(
            'No body provided. Please provide a JSON body.',
            status_code=400
        )
    else:
        author_id = req_body.get('author_id')
        course_id = req_body.get('course_id')
        document_id = req_body.get('document_id')
        ticket_type = req_body.get('ticket_type')
        description = req_body.get('description')
        assignee = req_body.get('assignee')

    # Check if all required parameters are available
    if not all([author_id, course_id, document_id, ticket_type, description]):
        return func.HttpResponse(
            "Missing required parameters.",
            status_code=400)

    try:
        ticket_id = generate_ticket_number(),
        # Save information in CosmosDB
        ticket_doc = {
            'id': ticket_id[0],
            'author_id': author_id,
            'course_id': course_id,
            'document_id': document_id,
            'ticket_type': ticket_type,
            'description': description,
            'status': 'Neu',
            'createdAt': datetime.datetime.now().isoformat(),
            'assignee': assignee
        }

        ticket.set(func.Document.from_dict(ticket_doc))
        return func.HttpResponse(
            ticket_id[0],
            status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            f"Error creating ticket: {str(ex)}",
            status_code=500)
