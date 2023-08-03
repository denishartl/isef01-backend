import datetime
import azure.functions as func
import logging


def main(req: func.HttpRequest, ticket: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Versuchen Sie, den JSON-Payload aus dem Body der Anfrage zu extrahieren
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            'Invalid JSON payload',
            status_code=400
        )

    # Extrahieren Sie die Parameter aus dem JSON-Payload
    author_id = req_body.get('author_id')
    course_id = req_body.get('course_id')
    document_id = req_body.get('document_id')
    ticket_type = req_body.get('ticket_type')
    description = req_body.get('description')

    # Überprüfen Sie, ob alle Parameter im JSON-Payload vorhanden sind
    if not all([author_id, course_id, document_id, ticket_type, description]):
        return func.HttpResponse(
            "Missing required parameters.",
            status_code=400)

    try:
        # Save information in CosmosDB
        ticket_doc = {
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
            "Ticket created successfully.",
            status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            f"Error creating ticket: {str(ex)}",
            status_code=500)
