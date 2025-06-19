from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth
from medic_app.models import Users
from django.db import connection
import json
import logging

logger = logging.getLogger("medic_app.auth")
@csrf_exempt
@require_http_methods(["POST"])
def create_new_user(request):
    try:
        data = json.loads(request.body)

        password = data.get('password')
        email = data.get('email')
        
        logger.info(f"Email: {email}")
        
        # Basic validation
        if not email or not password:
            return JsonResponse({"error": "All fields (email, password) are required."}, status=400)

        if Users.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already in use."}, status=409)
        
        newuser = auth.create_user(email=email,password=password)
        
        logger.info(f"New user created with UID: {newuser.uid}")
    
        # Create user
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO users (id,email) VALUES('{newuser.uid}','{email}')")
            cursor.execute(f"INSERT INTO addresses (user_id) VALUES('{newuser.uid}')")

        return JsonResponse({
            "message": "User created successfully.",
            "user": {
                "id": newuser.uid,
                "email": email,
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_authenticated_user(request):
    try:
        data = json.loads(request.body)
        id_token = data['id_token']
        if not id_token:
            return JsonResponse({"error": "id_token are required."}, status=400) 
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        auth.delete_user(uid)
        with connection.cursor() as cursor:
            cursor.execute("DELETE TABLE USERS WHERE id = %s", [uid])
        return JsonResponse({
            "message": "User deleted successfully.",
            "user": {
                "id": id_token,
            }
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
