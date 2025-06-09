from django.http import JsonResponse,HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .upload_file import upload_photo
import json
import tempfile
import os
import logging

logger = logging.getLogger("medic_app.users")

@require_http_methods(["GET"])
def get_user_details(request:HttpRequest):
    try:
        uid = request.GET.get("uid")
        logger.info(f"uid: {uid}")
        if not uid:
            return JsonResponse({"error": "uid is required."}, status=400)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", [uid])
            row = cursor.fetchone()
            logger.info(f"row: {row}")
            if not row:
                return JsonResponse({"error": "User not found."}, status=404)
            columns = [col[0] for col in cursor.description]
            user_data = dict(zip(columns, row))
            
        return JsonResponse({"user": user_data}, status=200)

    except Exception as e:
        logger.exception("An error occurred while fetching user details.")
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["POST"])
def update_user_details(request:HttpRequest):
    try:
        data = json.loads(request.body)
        uid = data.get('uid')

        if not uid:
            return JsonResponse({"error": "uid is required."}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", [uid])
            row = cursor.fetchone()

            if not row:
                return JsonResponse({"error": "User not found."}, status=404)

            columns = [col[0] for col in cursor.description]
            user_data_db = dict(zip(columns, row))

            user_data = {}
            for key in columns:
                if key == 'id':
                    continue
                user_data[key] = data.get(key, user_data_db.get(key))
            user_email = user_data_db.get('email')

            set_clauses = []
            update_values = []

            for key, value in user_data.items():
                set_clauses.append(f"{key} = %s")
                update_values.append(value)

            if not set_clauses:
                return JsonResponse({"message": "No fields to update."}, status=400)

            update_query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s"
            update_values.append(uid)

            cursor.execute(update_query, update_values)

        return JsonResponse({"message": f"User {user_email} has been updated successfully."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request: HttpRequest):
    try:
        uid = request.POST.get('uid')
        photo = request.FILES.get('photo')
        category_type = request.POST.get('type')
        mime_type = request.POST.get('mime_type')
        logger.info(f"payload = {uid} , {photo} , {category_type} , {mime_type}")

        if not uid or not photo or not category_type or not mime_type:
            return JsonResponse({
                "error": "Missing required parameters (uid, photo, type, mime_type)"
            }, status=400)

        ext = mime_type.split('/')[1]
        
        logger.info(f"ext: {ext}")
        

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
            for chunk in photo.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        result = upload_photo(temp_file_path, uid, category_type)
        logger.info(f"result: {result}")
        profile_pic = f"https://drive.google.com/uc?export=view&id={result['id']}"
        
        os.remove(temp_file_path) 
        
        logger.info(f"profile_pic: {profile_pic}")

        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET profile_pic = %s WHERE id = %s", [profile_pic, uid])

        return JsonResponse({
            "message": "Image has been uploaded successfully."
        }, status=201)

    except Exception as e:
        logger.exception("Image upload failed")
        return JsonResponse({"error": str(e)}, status=500)

