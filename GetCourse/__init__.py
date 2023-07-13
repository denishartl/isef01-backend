import azure.functions as func
import json


def main(req: func.HttpRequest, course: func.DocumentList) -> func.HttpResponse:
    course_param_id = req.params.get('id')
    
# Get course from CosmosDB via ticket_id
    course_doc = {
        'id': course[0]['id'],
        'shortname': course[0]['shortname'],
        'name': course[0]['name']    
    }

    # Course output
    return func.HttpResponse(
        json.dumps(course_doc),
        status_code=200
    )