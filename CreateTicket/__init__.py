import datetime
import azure.functions as func
import logging
import uuid


def main(req: func.HttpRequest, 
         ticket: func.Out[func.Document]) -> func.HttpResponse:
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

    # Check if all required parameters are available
    if not all([author_id, course_id, document_id, ticket_type, description]):
        return func.HttpResponse(
            "Missing required parameters.",
            status_code=400)

    try:
        ticket_id = str(uuid.uuid4()),
        # Save information in CosmosDB
        ticket_doc = {
            'id': ticket_id[0],
            'author_id': author_id,
            'course_id': course_id,
            'document_id': document_id,
            'ticket_type': ticket_type,
            'description': description,
            'status': 'new',
            'createdAt': datetime.datetime.utcnow().isoformat()
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
