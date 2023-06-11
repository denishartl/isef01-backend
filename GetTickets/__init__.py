import logging

import azure.functions as func


def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:

    return func.HttpResponse(documents.data[0].to_json())

