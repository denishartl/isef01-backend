import logging

import azure.functions as func


def main(req: func.HttpRequest, courses: func.DocumentList) -> func.HttpResponse:
    
    return func.HttpResponse(courses.data[0].to_json())
