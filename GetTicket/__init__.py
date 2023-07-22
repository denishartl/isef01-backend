import azure.functions as func
import json
import logging

"""
Selects a ticket out of Aure CosmosDB

"""
def main(req: func.HttpRequest, ticket: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ticket_id = req.params.get('id')
    if not ticket_id:
        return func.HttpResponse(
            "Please insert ticket ID.",
            status_code=400
        )
    
    if not ticket:
        return func.HttpResponse(
            "Could not find a ticket with the ID {ticket_id}.",
            status_code=400
        )

    else:
        try:
            # Get ticket from CosmosDB via ticket_id
            ticket_doc = {
                'id': ticket[0]['id'],
                'author_id': ticket[0]['author_id'],
                'course_id': ticket [0]['course_id'],
                'document_id': ticket [0]['document_id'],
                'ticket_type': ticket [0]['ticket_type'],
                'description': ticket [0]['description'],
                'status': ticket [0]['status'],
                'createdAt': ticket [0]['createdAt']
                
            }

            # Returns the ticket data as http response
            return func.HttpResponse(
                json.dumps(ticket_doc),
                status_code=200
        )

        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
            "Error finding ticket ID",
            status_code=500
            )


