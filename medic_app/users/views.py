from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json


@require_http_methods(["GET"])
def get_user_details(request):
    try:
        uid = request.GET.get("uid")
        if not uid:
            return  JsonResponse({"error": "uid is required."}, status=400)
        with connection.cursor() as cursor:
          cursor.execute("SELECT * FROM users WHERE id = %s", [uid])
          row = cursor.fetchone() 
        if not row:
           return JsonResponse({"error": "User not found."}, status=404)
        else:
            columns = [col[0] for col in cursor.description]
            user_data = dict(zip(columns, row))
          
        return JsonResponse({
            "user": user_data
        }, status=200)
        
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
    
@csrf_exempt
@require_http_methods(["POST"])
def update_user_details(request):
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

        return JsonResponse({"message": f"User {uid} has been updated successfully."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
