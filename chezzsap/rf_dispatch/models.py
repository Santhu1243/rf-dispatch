from django.db import models
from django.contrib.auth.models import User
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StorageLocation(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.warehouse.name})"


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit_of_measure = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    reorder_level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class InboundOrder(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    supplier_name = models.CharField(max_length=100)
    supplier_contact = models.CharField(max_length=100)
    received_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Received', 'Received')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class InboundOrderItem(models.Model):
    inbound_order = models.ForeignKey(InboundOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OutboundOrder(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=100)
    shipment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class OutboundOrderItem(models.Model):
    outbound_order = models.ForeignKey(OutboundOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    quantity_shipped = models.PositiveIntegerField(default=0)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    quantity_on_hand = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'warehouse', 'storage_location')


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('Inbound', 'Inbound'),
        ('Outbound', 'Outbound'),
        ('Transfer', 'Transfer'),
        ('Adjustment', 'Adjustment'),
    ]
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_location = models.ForeignKey(StorageLocation, related_name='movement_from', on_delete=models.SET_NULL, null=True, blank=True)
    to_location = models.ForeignKey(StorageLocation, related_name='movement_to', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    reference_order = models.CharField(max_length=100, null=True, blank=True)
    reason = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product.sku} - {self.quantity}"


from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class DispatchSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outbound_order = models.ForeignKey('OutboundOrder', on_delete=models.CASCADE)
    dock_door = models.CharField(max_length=50)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class HandlingUnit(models.Model):
    hu_code = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    outbound_order_item = models.ForeignKey('OutboundOrderItem', on_delete=models.CASCADE)
    is_scanned = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(null=True, blank=True)
