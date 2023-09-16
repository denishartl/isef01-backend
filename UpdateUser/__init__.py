import azure.functions as func
import logging

def main(req: func.HttpRequest, 
         user: func.DocumentList, 
         outuser: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        user_id = req.params.get('user_id')
        if not user_id:
            return func.HttpResponse(
                "Please provide a user ID to query for.",
                status_code=400
            )

        # Check if other requested parameters from the body exist
        try:
            req_body = req.get_json()
        except ValueError as ex:
            logging.error(ex)
            return func.HttpResponse(
                'No body provided. Please provide a request body.',
                status_code=500
            )

        # Get the user from Cosmos DB
        if user:
            user_item = user[0]

            # Update user data
            user_password = req_body.get('password')
            if user_password:
                user_item['password'] = user_password

            user_surname = req_body.get('surname')
            if user_surname:
                user_item['surname'] = user_surname

            user_lastname = req_body.get('lastname')
            if user_lastname:
                user_item['lastname'] = user_lastname

            user_role = req_body.get('role')
            if user_role:
                user_item['role'] = user_role

            # Save the updated ticket
            outuser.set(user_item)

            return func.HttpResponse(
                'User updated successfully',
                status_code=200
            )
        else:
            return func.HttpResponse(
                'user not found',
                status_code=404
            )

    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )