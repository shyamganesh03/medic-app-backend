from django.http import JsonResponse,HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import logging

logger = logging.getLogger("medic_app.products")


# Create your views here.

@require_http_methods(['GET'])
def get_categories_list(request:HttpRequest):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM categories")
            rows = cursor.fetchall()
            if not rows:
                return JsonResponse({"categories": []}, status=200)

            columns = [col[0] for col in cursor.description]
            categories_data = [dict(zip(columns, row)) for row in rows]

        return JsonResponse({"categories": categories_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(['GET'])
def get_product_list(request:HttpRequest):      
    try:
      with connection.cursor() as cursor:
          cursor.execute("SELECT * FROM products")
          rows = cursor.fetchall()
          if not rows:
             return JsonResponse({
              "products": []
          }, status=200)
             
          else:
              columns = [col[0] for col in cursor.description]
              products_data = [dict(zip(columns, row)) for row in rows]
        
      return JsonResponse({
          "products": products_data
      }, status=200)
      
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
      

@require_http_methods(['GET'])
def get_product_list_by_category_id(request:HttpRequest):
    try:
        category_id = request.GET.get('category_id')
        logger.info(f"category_id = {category_id}")
        if not category_id:
           return  JsonResponse({"error": "category_id is required."}, status=400)         
       
        with connection.cursor() as productCursor:
          productCursor.execute("SELECT p.id AS product_id, p.name AS product_name, p.description, p.price, p.discount, p.available_stock, p.created_at, p.updated_at, c.id AS category_id, c.name AS category_name FROM products p INNER JOIN categories c ON p.category_id = c.id WHERE p.category_id = %s", [category_id])
          rows = productCursor.fetchall() 
          
          if not rows:
             return JsonResponse({"error": "product not found."}, status=404)
          else:
              columns = [col[0] for col in productCursor.description]
              products_data = [dict(zip(columns, row)) for row in rows]
    
        return JsonResponse({
            "items": products_data
        }, status=200)
    
    except Exception as e:
         return JsonResponse(
             {
              "error": "product not found.",
              "errorMessage": str(e)
             },
             status=500)

@csrf_exempt
@require_http_methods(['POST'])
def add_products_bulk(request: HttpRequest):
    try:
        product_data = json.loads(request.body)
        items: list = product_data.get("items", [])
        
        if not items:
            return JsonResponse({"error": "No items provided"}, status=400)

        fields = list(items[0].keys())
        field_values = [
            [item[field] for field in fields]
            for item in items
        ]

        # Batch insert in chunks of 100
        batch_size = 100
        placeholders = "(" + ", ".join(["%s"] * len(fields)) + ")"
    
        with connection.cursor() as cursor:
            for i in range(0, len(field_values), batch_size):
                batch = field_values[i:i + batch_size]
                flat_values = [val for record in batch for val in record]
                dynamic_query = f"INSERT INTO products ({', '.join(fields)}) VALUES " + \
                                ", ".join([placeholders] * len(batch))
                cursor.execute(dynamic_query, flat_values)

        return JsonResponse({"status": "success"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)