import datetime
import logging
import os
import azure.functions as func
from #azureblobstorage

"""
Creates a ticket and saves it to Azure CosmosDB together with the following data:

- author ID
- course ID
- document ID
- tickettype
- description
- status (auto)
- createdAt (auto)


To Do: Statuscodes; Speichern in CosmosDB

"""

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        author_id = req_body.get('author_id')
        course_id = req_body.get('course_id')
        document_id = req_body.get('document_id')
        ticket_type = req_body.get('ticket_type')
        description = req_body.get('description')


# Ticket in der CosmosDB speichern
ticket = {
    'author_id': author_id,
    'course_id': course_id,
    'document_id': document_id,
    'ticket_type': ticket_type,
    'description': description,
    'status': #auto,
    'createdAt': datetime.datetime.utcnow().isoformat()
}