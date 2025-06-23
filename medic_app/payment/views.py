
from django.http import JsonResponse,HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import logging
from constant import fields_meta_data
from datetime import datetime


logger = logging.getLogger("medic_app.payment")

card_details_fields = fields_meta_data.card_details_fields

@csrf_exempt
@require_http_methods(["POST"])
def update_user_payment_method(request: HttpRequest):
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
        card_details = data.get('card_details')
        current_time_stamp = datetime.now()
        
        logger.info(f"uid: {uid}")
        logger.info(f"card_details: {card_details}")

        if not uid or not card_details:
            return JsonResponse({"error": "uid and card_details are required."}, status=400)
        
        for field in card_details:
            if field not in card_details_fields:
                return JsonResponse({"error": f"Some of the fields are missing {card_details_fields}."}, status=400)
            else:
                continue
        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE user_payment_management SET card_details = %s, updated_at = %s WHERE user_id = %s",[json.dumps(card_details),current_time_stamp,uid])
            
        return JsonResponse({
            "message": "User payment method updated successfully."
            },
            status=200)
        
    except Exception as e:
        logger.exception("An error occurred while fetching user details.")
        return JsonResponse({"error": str(e)}, status=500)
    
    
@require_http_methods(['GET'])
def get_user_payment_method_details(request: HttpRequest):
    try:
        uid = request.GET.get('uid')
        if not uid:
            return JsonResponse({"error": "uid is required."}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_payment_management WHERE user_id = %s", [uid])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({"error": "User payment method not found."}, status=404)

            columns = [col[0] for col in cursor.description]
            card_details = dict(zip(columns, row))

        return JsonResponse({"payment_details": card_details}, status=200)

    except Exception as e:
        logger.exception("An error occurred while fetching user payment method.")
        return JsonResponse({"error": str(e)}, status=500)