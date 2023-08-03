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

def main(req: func.HttpRequest, ticket: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
        
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
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            'Invalid JSON payload',
            status_code=400
    )
     
    else:
        author_id = req_body.get('author_id')
        course_id = req_body.get('course_id')
        document_id = req_body.get('document_id')
        ticket_type = req_body.get('ticket_type')
        description = req_body.get('description')
    
    # Return HTTP errors if something of the body is missing
    try:
        if not author_id:
             return func.HttpResponse(
                  'No author ID provided. Please enter author ID when using this function.',
                  status_code=400
             )
        if not course_id:
             return func.HttpResponse(
                  'No course ID provided. Please enter course ID when using this function.',
                  status_code=400
             )
        if not document_id:
             return func.HttpResponse(
                  'No document ID provided. Please enter document ID when using this function.',
                  status_code=400
             )
        if not ticket_type:
             return func.HttpResponse(
                  'No ticket type  provided. Please enter ticket type when using this function.',
                  status_code=400
             )
        if not description:
             return func.HttpResponse(
                  'No description provided. Please enter a description when using this function.',
                  status_code=400
             )

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