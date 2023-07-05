import azure.functions as func
import json

"""
Selects a ticket out of Aure CosmosDB

"""
def main(req: func.HttpRequest, ticket: func.Out[func.Document]) -> func.HttpResponse:
    ticket_id = req.params.get('id')


    # Get ticket from CosmosDB via ticket_id
    ticket_doc = {
        'id': ticket[0]['id'],
    }

    

    # Rückgabe der Ticketdaten in der HTTP-Antwort
    return func.HttpResponse(json.dumps(ticket))