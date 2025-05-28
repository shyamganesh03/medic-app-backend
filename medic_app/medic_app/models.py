# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActivityLogs(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_logs'


class Addresses(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    type = models.CharField(max_length=20, blank=True, null=True)
    house_no = models.CharField(max_length=50, blank=True, null=True)
    street_name = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class Categories(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class OrderItems(models.Model):
    id = models.UUIDField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    products = models.JSONField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    shop_vendor_id = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Payments(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    invoice_number = models.TextField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments'


class Products(models.Model):
    id = models.UUIDField(primary_key=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    available_stock = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class UserPaymentManagement(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    payment_method = models.TextField(blank=True, null=True)
    upi_id = models.TextField(blank=True, null=True)
    credit_card_details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_payment_management'


class Users(models.Model):
    id = models.UUIDField(primary_key=True)
    full_name = models.CharField(max_length=500)
    email = models.CharField(unique=True, max_length=500)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    house_no = models.CharField(max_length=50, blank=True, null=True)
    street_name = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    is_phone_number_verified = models.BooleanField(blank=True, null=True)
    is_email_verified = models.BooleanField(blank=True, null=True)
    role = models.CharField(max_length=20)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    address_type = models.CharField(max_length=100, blank=True, null=True)
    shop_name = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
