import azure.functions as func
import json
import logging

"""

Returns a list of tickets based on the ticket ID

Needed parameter: id (ticket)

"""

def main(req: func.HttpRequest, tickets: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.max_retry_count)

    if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")

    ticket_id = req.params.get('id')
    
    try:
            # Returns a list of all tickets
                ticket_list = []
                for ticket in tickets:
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

