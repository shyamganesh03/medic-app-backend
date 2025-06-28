from django.http import JsonResponse,HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
import json
import logging
import requests
import uuid
from datetime import datetime, timedelta, timezone

# curl --request POST 
#     --url https://sandbox.cashfree.com/pg/orders 
#     --header 'x-client-id: TEST430329ae80e0f32e41a393d78b923034'
#     --header 'x-client-secret: TESTaf195616268bd6202eeb3bf8dc458956e7192a85'
#     --header 'Accept: application/json' 
#     --header 'Content-Type: application/json' 
#     --header 'x-api-version: 2025-01-01' 
#     --data '{
#     "order_amount": 1.00,
#     "order_currency": "INR",
#     "order_id": "devstudio_7344521686389347997",
#     "customer_details": {
#         "customer_id": "devstudio_user",
#         "customer_phone": "8474090589",
#         "customer_name": "Harshith",
#         "customer_email": "test@cashfree.com"
#     },
#     "order_meta": {
#         "return_url": "https://www.cashfree.com/devstudio/preview/pg/mobile/hybrid?order_id={order_id}",
#         "payment_methods": "cc,dc,upi"
#     },
#     "cart_details": {
#         "cart_items": [
#             {
#                 "item_id": "devstudio_cart_id",
#                 "item_name": "Shoes",
#                 "item_description": "Durable, comfortable, and perfect for adding personality to any outfit.",
#                 "item_image_url": "https://cashfreelogo.cashfree.com/website/landings-cache/landings/occ/brownShoe.png",
#                 "item_original_unit_price": 1.00,
#                 "item_discounted_unit_price": 1.00,
#                 "item_quantity": 1,
#                 "item_currency": "INR"
#             }
#         ]
#     },
#     "order_expiry_time": "2025-06-29T00:28:23.920Z"
# }'

logger = logging.getLogger("medic_app.orders")

x_client_id= 'TEST430329ae80e0f32e41a393d78b923034'
x_client_secret= 'TESTaf195616268bd6202eeb3bf8dc458956e7192a85'
x_api_version= '2025-01-01'
payment_url= 'https://sandbox.cashfree.com/pg'

headers = {
    "x-api-version": x_api_version,
    "x-client-id": x_client_id,
    "x-client-secret": x_client_secret,
    "Content-Type": "application/json"
}



@csrf_exempt
@require_http_methods(['POST'])
def create_order(request: HttpRequest):
    try:
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        cart_items = data.get('cart_items')
        total_amount = data.get('total_amount')
        currency = data.get('currency')
        
        logger.info(f"Payloads Data = {customer_id,cart_items,total_amount,currency}")
        
        if not customer_id or not cart_items or not total_amount or not currency:
            return JsonResponse({"error":"some fields are missing customer_id, cart_items, total_amount, currency"},status=500)

        # Fetch user
        with connection.cursor() as cursor:
            cursor.execute('SELECT full_name, email, phone_number FROM users WHERE id = %s', [customer_id])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({"error": "User not found."}, status=404)
            columns = [col[0] for col in cursor.description]
            user_data = dict(zip(columns, row))

        customer_details = {
            "customer_id": customer_id,
            "customer_phone": user_data['phone_number'],
            "customer_name": user_data['full_name'],
            "customer_email": user_data['email']
        }
        
        logger.info(f"Customer Details {customer_details}")

        order_id = str(uuid.uuid4())
        order_expiry_time = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat().replace('+00:00', 'Z')
        
        logger.info(f"orders {order_id} {order_expiry_time}")

        payload = {
            "order_amount": total_amount,
            "order_currency": currency,
            "order_id": order_id,
            "customer_details": customer_details,
            "order_meta": {
                "return_url": f"https://www.cashfree.com/devstudio/preview/pg/mobile/hybrid?order_id={order_id}",
                "payment_methods": "cc,dc"
            },
            "cart_details": {
                "cart_items": cart_items
            },
            "order_expiry_time": order_expiry_time
        }
        
        logger.info(f"Payload: {payload}")

        create_order_response = requests.post(f'{payment_url}/orders', json=payload, headers=headers)
        
        logger.info(f"create_order_response {create_order_response.text}")
        if create_order_response.status_code != 200:
            return JsonResponse({"error": "order creation failed.", "details": create_order_response.text}, status=500)

        order_item_ids = []
        products_quantity_data = []

        # Use a transaction to make sure all DB changes happen atomically
        with transaction.atomic():
            with connection.cursor() as cursor:
                for item in cart_items:
                    order_item_id = str(uuid.uuid4())
                    order_item_ids.append(order_item_id)
                    item_id = item['product_id']
                    item_quantity = item['quantity']
                    decremented_item_quantity = item['available_stock'] - item_quantity
                    price = item['price']
                    products_quantity_data.append({"id": item_id,"qty": decremented_item_quantity})

                    cursor.execute('''
                       INSERT INTO order_items (id, order_id, product_id, quantity,amount)
                       VALUES (%s, %s, %s, %s, %s)
                   ''', [
                       order_item_id,
                       order_id,
                       item_id,
                       item_quantity,
                       price
                   ])
                
                order_uid = str(uuid.uuid4())
                
                json_order_ids = json.dumps({ "ids": order_item_ids})
                
                logger.info(f"json_order_ids: {json_order_ids}")
                
                cursor.execute('''
                    INSERT INTO orders (id, user_id, status, cf_order_id, net_amount, discount, currency, final_amount, order_items_ids)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', [
                    order_uid,
                    customer_id,
                    'created',
                    order_id,
                    total_amount,
                    0.0,
                    currency,
                    total_amount,
                    json_order_ids
                ])
                for p in products_quantity_data:
                 cursor.execute(
                     '''
                     UPDATE products
                     SET available_stock = %s
                     WHERE id = %s
                     ''',
                     [p['qty'], p['id']]
                 )

        return JsonResponse({
            "message": "Order created successfully",
            "order_id": order_id,
            "order_item_ids": order_item_ids,
            "cf_order_response": create_order_response.json()
        }, status=201)

    except Exception as e:
        logger.exception("Error in create_order")
        return JsonResponse({"error": str(e)}, status=500)
