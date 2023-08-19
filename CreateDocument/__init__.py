import logging
import uuid

import azure.functions as func

"""
This function creates a new document in the database based on the data passed in the JSON
body. 

Expected query parameters:
None

Expected content in the JSON body:
* document_title: Title of the document
* document_doctype: Type of the document (script, video, ....)
* document_course: ID of the course to which the document is assigned to
"""

def main(req: func.HttpRequest, document: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Check if every expected part of the request body exists
    try:
        req_body = req.get_json()
        if type(req_body) is str:
            return func.HttpResponse(
                'Body is not in JSON format. Please provide a valid JSON formated body.',
                status_code=400
            )
    except AttributeError:
        return func.HttpResponse(
                'No body provided. Please provide a JSON body.',
                status_code=400
            )
    else:
        document_title = req_body.get('document_title')
        document_doctype = req_body.get('document_doctype') 
        document_course = req_body.get('document_course') 

    # Return HTTP errors if one part of the body is missing
    try:
        if not document_title:
            return func.HttpResponse(
                'No document title provided. Please provide a document title in the body when calling this function.',
                status_code=400
            )
        if not document_doctype:
            return func.HttpResponse(
                'No doctype provided. Please provide a doctype in the body when calling this function.',
                status_code=400
            )
        if not document_course:
            return func.HttpResponse(
                'No course provided. Please provide a course in the body when calling this function.',
                status_code=400
            )
    
        # Save information to Azure CosmosDB
        document_dict = {
            'id': str(uuid.uuid4()),
            'title': document_title,
            'doctype': document_doctype,
            'course': document_course
        }

        document.set(func.Document.from_dict(document_dict))
        return func.HttpResponse(
                status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )
