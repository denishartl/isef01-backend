import os
import logging

import azure.functions as func
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient

"""
This function deletes the attachment specified in the query parameter:

Expected query parameters:
* attachment_id: ID of the attachment to delete
"""

def main(req: func.HttpRequest, attachment: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    attachment_id = req.params.get('attachment_id')
    if not attachment_id:
        return func.HttpResponse(
            "Please provide a attachment ID to delete.",
            status_code=400
        )
    try:
        ENDPOINT = os.environ["COSMOS_ENDPOINT"]
        KEY = os.environ["COSMOS_KEY"]
        DATABASE_NAME = "isef01"
        CONTAINER_NAME = "attachment"

        client = CosmosClient(url=ENDPOINT, credential=KEY)
        database = client.create_database_if_not_exists(id=DATABASE_NAME)
        key_path = PartitionKey(path="/id")
        container = database.create_container_if_not_exists(
            id=CONTAINER_NAME, partition_key=key_path
        )

        response = container.delete_item(item=attachment_id, partition_key=attachment_id)

        blob_connect_string = os.getenv('BLOB_CONNECT_STRING')
        blob_container = os.getenv('BLOB_CONTAINER')


        blob_service_client = BlobServiceClient.from_connection_string(blob_connect_string)
        blob_client = blob_service_client.get_blob_client(container=blob_container,blob=attachment[0]['uuid'])
        blob_client.delete_blob()

        if not response:
            return func.HttpResponse(
                    'Deleted ticket successfully.',
                    status_code=200
                )
        else:
            return func.HttpResponse(
                    'Error deleting ticket.',
                    status_code=500
                )
    except Exception:
        return func.HttpResponse(
                    'Error deleting ticket.',
                    status_code=500
                )
