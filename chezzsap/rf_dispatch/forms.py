from django import forms
from .models import (
    Warehouse, StorageLocation, Product,
    InboundOrder, InboundOrderItem,
    OutboundOrder, OutboundOrderItem,
    Inventory, StockMovement, DispatchSession, HandlingUnit
)

# Reusable date/datetime widget functions
def date_input_widget():
    return forms.DateInput(attrs={'type': 'date'})

def datetime_input_widget():
    return forms.DateTimeInput(attrs={'type': 'datetime-local'})


# Base form for Bootstrap styling
class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class WarehouseForm(BaseStyledForm):
    class Meta:
        model = Warehouse
        fields = '__all__'


class StorageLocationForm(BaseStyledForm):
    class Meta:
        model = StorageLocation
        fields = '__all__'


class ProductForm(BaseStyledForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'sku': forms.TextInput(attrs={'placeholder': 'Stock Keeping Unit'}),
            'name': forms.TextInput(attrs={'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'unit_of_measure': forms.TextInput(attrs={'placeholder': 'e.g. kg, pcs'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category'}),
            'reorder_level': forms.NumberInput(attrs={'min': 0}),
        }


class InboundOrderForm(BaseStyledForm):
    class Meta:
        model = InboundOrder
        fields = '__all__'
        widgets = {
            'received_date': date_input_widget(),
        }


class InboundOrderItemForm(BaseStyledForm):
    class Meta:
        model = InboundOrderItem
        fields = '__all__'

    def clean_quantity_ordered(self):
        qty = self.cleaned_data.get('quantity_ordered')
        if qty <= 0:
            raise forms.ValidationError("Quantity ordered must be greater than zero.")
        return qty


class OutboundOrderForm(BaseStyledForm):
    class Meta:
        model = OutboundOrder
        fields = '__all__'
        widgets = {
            'shipment_date': date_input_widget(),
        }


class OutboundOrderItemForm(BaseStyledForm):
    class Meta:
        model = OutboundOrderItem
        fields = '__all__'

    def clean_quantity_ordered(self):
        qty = self.cleaned_data.get('quantity_ordered')
        if qty <= 0:
            raise forms.ValidationError("Quantity ordered must be greater than zero.")
        return qty


class InventoryForm(BaseStyledForm):
    class Meta:
        model = Inventory
        fields = '__all__'

    def clean_quantity_on_hand(self):
        qty = self.cleaned_data.get('quantity_on_hand')
        if qty < 0:
            raise forms.ValidationError("Inventory quantity cannot be negative.")
        return qty


class StockMovementForm(BaseStyledForm):
    class Meta:
        model = StockMovement
        exclude = ['timestamp']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
            'reference_order': forms.TextInput(attrs={'placeholder': 'Optional reference'}),
        }


class DispatchSessionForm(BaseStyledForm):
    class Meta:
        model = DispatchSession
        fields = '__all__'
        widgets = {
            'started_at': datetime_input_widget(),
            'completed_at': datetime_input_widget(),
        }


class HandlingUnitForm(BaseStyledForm):
    class Meta:
        model = HandlingUnit
        fields = '__all__'
        widgets = {
            'hu_code': forms.TextInput(attrs={'placeholder': 'Handling Unit Code'}),
        }
