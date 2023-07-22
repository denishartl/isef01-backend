import datetime
import azure.functions as func
import logging


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

def main(req: func.HttpRequest, ticket: func.Out[func.Document], context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.retry_count)

    if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")
        
    author_id = req.params.get('author_id')
    course_id = req.params.get('course_id')
    document_id = req.params.get('document_id')
    ticket_type = req.params.get('ticket_type')
    description = req.params.get('description')
 
    if not all([author_id, course_id, document_id, ticket_type, description]):
        return func.HttpResponse(
            "Missing required parameters.", 
            status_code=400)
    
    try:
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
            "Ticket created successfully.", 
            status_code=200)

    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error creating ticket: {str(ex)}", 
            status_code=500)