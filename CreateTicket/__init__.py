import datetime
import azure.functions as func


"""
Creates a ticket and saves it to Azure CosmosDB together with the following data:

- author ID
- course ID
- document ID
- tickettype
- description
- status (new)
- createdAt (auto)


"""

def main(req: func.HttpRequest, ticket: func.Out[func.Document]) -> func.HttpResponse:
    author_id = req.params.get('author_id')
    course_id = req.params.get('course_id')
    document_id = req.params.get('document_id')
    ticket_type = req.params.get('ticket_type')
    description = req.params.get('description')
 


    # Save Ticket in CosmosDB 
    ticket_doc = {
        'author_id': author_id,
        'course_id': course_id,
        'document_id': document_id,
        'ticket_type': ticket_type,
        'description': description,
        'status': 'new',
        'createdAt': datetime.datetime.utcnow().isoformat()
    }

    # Save information to Azure CosmosDB
    ticket.set(func.Document.from_dict(ticket_doc))

    return func.HttpResponse(
                status_code=200
        )