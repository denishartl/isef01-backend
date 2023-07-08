import azure.functions as func
import json

"""
Selects a ticket out of Aure CosmosDB

"""
def main(req: func.HttpRequest, ticket: func.DocumentList) -> func.HttpResponse:
    ticket_param_id = req.params.get('id')


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

    # Rückgabe der Ticketdaten in der HTTP-Antwort
    return func.HttpResponse(
        json.dumps(ticket_doc),
        status_code=200
    )