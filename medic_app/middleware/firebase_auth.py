import logging
from django.http import JsonResponse,HttpRequest
from firebase_admin import auth

logger = logging.getLogger("medic_app.middleware")


excluded_path = [
    '/authentication/create_new_user'
]

class medic_middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request:HttpRequest):
        logger.info(f"path: {request.path}")
        if request.path in excluded_path:
            logger.info(f"Skipping authentication for path: {request.path}")
            return self.get_response(request)
        
        authorization_header = request.headers.get('Authorization')
        logger.info(f"Authorization Header: {authorization_header}")
        if(authorization_header is None or authorization_header.startswith("Bearer") is False):
            logger.error("Authorization token is missing.")
            return JsonResponse({"error": "Authorization token is missing."}, status=500)
        try:
            id_token = authorization_header.split(" ")[1]
            logger.info(f"ID Token: {id_token}")
            user = auth.verify_id_token(id_token)
            request.user_token = user
            
        except Exception as e:
            logger.error(f"Error on MiddleWare: {str(e)}")
            return JsonResponse({"error": "Unauthorized User."}, status=401)

        return self.get_response(request)
