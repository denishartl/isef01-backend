import datetime
import logging

import azure.functions as func

"""
This function updates a comment in CosmosDB with the new text provided in the request.

Expected query parameters:
* comment_id: ID of the comment which should be edited

Expected query body:
* text: New text of the comment

"""


def main(req: func.HttpRequest,
         comment: func.DocumentList,
         outcomment: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        comment_id = req.params.get('comment_id')
        if not comment_id:
            return func.HttpResponse(
                "Please provide a comment ID to query for.",
                status_code=400
            )
        # Check if every expected part of the request body exists
        try:
            req_body = req.get_json()
        except ValueError as ex:
            logging.error(ex)
            return func.HttpResponse(
                'No body provided. Please provide request body.',
                status_code=500
            )
        else:
            text = req_body.get('text')

        if not text:
            return func.HttpResponse(
                'No text provided. Please pass a text in the body when calling this function.',
                status_code=400
            )

        if comment:
            comment = comment[0]

            comment.data['text'] = text
            comment.data['changedAt'] = datetime.datetime.utcnow().isoformat()

            outcomment.set(comment)

            return func.HttpResponse(
                'Comment updated successfully',
                status_code=200
            )
        else:
            return func.HttpResponse(
                f"Could not find any comment with ID {comment_id}.",
                status_code=400
            )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )
