from django.http import JsonResponse,HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .upload_file import upload_photo
import json
import tempfile
import os
import logging
from constant import address_table_fields

logger = logging.getLogger("medic_app.users")

@require_http_methods(["GET"])
def get_user_details(request:HttpRequest):
    try:
        uid = request.GET.get("uid")
        logger.info(f"uid: {uid}")
        if not uid:
            return JsonResponse({"error": "uid is required."}, status=400)
        
        
        with connection.cursor() as cursor:
            cursor.execute("""
                           select u.id, u.full_name, u.email, u.profile_pic, u.phone_number, u.calling_code, u.country, u.shop_name, 
                           u.is_phone_number_verified, u.is_email_verified, u."role",u.is_active, a.id as address_id, a.user_id,a."type",
                           a.house_no,a.address_line_1, a.city,a.state,a.postal_code,a.country, a.is_default from users u inner join addresses a 
                           on u.id = a.user_id where u.id = %s ;
                           """, [uid]
                           )
            row = cursor.fetchone()
            logger.info(f"row: {row}")
            if not row:
                return JsonResponse({"error": "User not found."}, status=404)
            columns = [col[0] for col in cursor.description]
            user_data = dict(zip(columns, row))
            
            address_data = {}
            new_user_data = {}
            
            for key, value in user_data.items():
                if key in address_table_fields.address_fields or key == 'address_id':
                    address_data[key if key != 'address_id' else 'id'] = value
                else:
                    new_user_data[key] = value
            if new_user_data:
             new_user_data['address'] = address_data
            
        return JsonResponse({"user": new_user_data}, status=200)

    except Exception as e:
        logger.exception("An error occurred while fetching user details.")
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["POST"])
def update_user_details(request: HttpRequest):
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
        logger.info(f"uid: {uid}")
        if not uid:
            return JsonResponse({"error": "uid is required."}, status=400)

        with connection.cursor() as cursor:
            
            cursor.execute("SELECT * FROM users WHERE id = %s", [uid])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({"error": "User not found."}, status=404)

            user_columns = [col[0] for col in cursor.description]
            user_data_db = dict(zip(user_columns, row))

            user_data = {
                key: data.get(key, user_data_db.get(key))
                for key in user_columns if key != 'id'
            }

            set_clauses = [f"{key} = %s" for key in user_data]
            update_values = list(user_data.values())
            update_values.append(uid)

            address = data.get('address')
            if address:
                cursor.execute("SELECT * FROM addresses WHERE user_id = %s", [uid])
                address_row = cursor.fetchone()
                user_address_db = {}
                if address_row:
                    address_columns = [col[0] for col in cursor.description]
                    user_address_db = dict(zip(address_columns, address_row))

                address_data = {
                    key: address.get(key, user_address_db.get(key))
                    for key in address_table_fields.address_fields
                }

                set_address_clauses = [f"{key} = %s" for key in address_data]
                update_or_create_values = list(address_data.values())

                if address_row:
                    update_or_create_values.append(uid)
                    address_query = f"""
                        UPDATE addresses
                        SET {', '.join(set_address_clauses)}
                        WHERE user_id = %s
                    """
                else:
                    address_query = f"""
                        INSERT INTO addresses ({', '.join(address_data.keys())})
                        VALUES ({', '.join(['%s'] * len(address_data))})
                    """

                logger.info(f"Executing address query: {address_query} with {update_or_create_values}")
                cursor.execute(address_query, update_or_create_values)

            update_query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s"
            logger.info(f"Executing user update query: {update_query} with {update_values}")
            cursor.execute(update_query, update_values)

        return JsonResponse({"message": f"User {user_data_db.get('email')} has been updated successfully."}, status=200)

    except Exception as e:
        logger.exception("Error updating user details")
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

