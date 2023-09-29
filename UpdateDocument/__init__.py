import azure.functions as func
import logging


def main(req: func.HttpRequest, document: func.DocumentList, outdocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        doc_item = document[0]

        old_doctype = doc_item['doctype']
        if old_doctype == 'script':
            doc_item['doctype'] = 'Skript'
        elif old_doctype == 'video':
            doc_item['doctype'] = 'Video'

        outdocument.set(doc_item)

        return func.HttpResponse(status_code=200)
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )
