import datetime
import azure.functions as func
import json
import logging


def main(req: func.HttpRequest, 
         ticket: func.DocumentList, 
         outticket: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        ticket_id = req.params.get('id')
        if not ticket_id:
            return func.HttpResponse(
                # DH: Status Code fehlt. Du bist wahrscheinlich bei deinen Tests immer hier rein gelaufen, hast aber HTTP 200 zurück bekommen, weil du keinen Status Code mitgibst
                "Please provide a Ticket ID to query for.",
            ) 
        # Check if ervery requested parameter of the body exists
        try:
            # DH: Variablenname ist hier denke ich falsch. Der wird weiter unten nie verwendet
            # DH: Außerdem prüfst du hier ja den Body. Die ticket-id wird ja als Parameter übergeben. Im Body erwartest du ja eigentlich author_id, course_id, usw. Du solltest also prüfen, ob die Einträge auch da sind
            ticket_doc = {
                    'id': ticket_id   
                }
            
            req_body = req.get_json()
        except ValueError as ex:
            logging.error(ex)
            return func.HttpResponse(
                'No body provided. Please provide request body.',
                status_code=400
            )
        else: 
            ticket_id = req_body.get('ticket_id')

        if not ticket_id:
            return func.HttpResponse(
                # DH: Text hier ist falsch
                'No text provided. Please pass a text in the body when calling this function.',
                status_code=400
            )

    # Get ticket from Cosmos DB
        if ticket:
            ticket_item = ticket[0]

        
            # Update ticket data
            author_id = req_body.get('author_id')
            if author_id:
                ticket_item['author_id'] = author_id

            course_id = req_body.get('course_id')
            if course_id:
                ticket_item['course_id'] = course_id

            document_id = req_body.get('document_id')
            if document_id:
                ticket_item['document_id'] = document_id

            ticket_type = req_body.get('ticket_type')
            if ticket_type:
                ticket_item['ticket_type'] = ticket_type

            description = req_body.get('description')
            if description:
                ticket_item['description'] = description

            status = req_body.get('status')
            if status:
                ticket_item['status'] = status
                if status == "closed":
                    ticket_item['resolvedAt'] = datetime.datetime.now().isoformat()

            outticket.set(ticket_item)

            return func.HttpResponse(
                'Ticket updated successfully',
                status_code=200
            )
        else:
            return func.HttpResponse(
            'Ticket not found',
            status_code=404
            )

    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
        status_code=500
        )