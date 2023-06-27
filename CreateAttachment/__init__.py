import base64
import logging
import os
import uuid

import azure.functions as func
from azure.storage.blob import BlobServiceClient

"""
This function uploads a file to Azure Blob Storage and saves it's link along with metadata to Azure CosmosDB:

Expected content in the JSON body:
* name: name of the file (e.g. "example.jpg") - can be any type of file
* ticket_id: ID of the ticket the file is associated to
* file: BASE64 encoded file, which should be uploaded
"""


def main(req: func.HttpRequest, attachment: func.Out[func.Document], context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.retry_count)

    if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")

    # Check if every expected part of the request body exists
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        name = req_body.get('name')
        ticket_id = req_body.get('ticket_id')
        file = req_body.get('file')

    # Return HTTP errors if one part of the body is missing
    try:
        if not name:
            return func.HttpResponse(
                'No name provided. Please pass a name in the body when calling this function.',
                status_code=400
            )
        if not ticket_id:
            return func.HttpResponse(
                'No ticket ID provided. Please pass a ticket ID in the body when calling this function.',
                status_code=400
            )
        if not file:
            return func.HttpResponse(
                'No file provided. Please pass a file in base64 encoded format in the body when calling this function.',
                status_code=400
            )
        
        # Upload file to blob storage and generate a UUID for it
        attachment_file = base64.b64decode(file)
        blob_connect_string = os.getenv('BLOB_CONNECT_STRING')
        blob_container = os.getenv('BLOB_CONTAINER')
        attachment_uuid = str(uuid.uuid1())

        blob_service_client = BlobServiceClient.from_connection_string(blob_connect_string)
        blob_client =blob_service_client.get_blob_client(container=blob_container,blob=attachment_uuid)
        blob_client.upload_blob(attachment_file)
        
        # Save information to Azure CosmosDB
        attachment_json = {
            'name': name,
            'ticket_id': ticket_id,
            'uuid': attachment_uuid,
            'blob_link': "https://iuisef01b10e.blob.core.windows.net/attachment/" + attachment_uuid
        }

        attachment.set(func.Document.from_dict(attachment_json))
        return func.HttpResponse(
                status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )

