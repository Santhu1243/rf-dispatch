from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import (
    Warehouse, StorageLocation, Product, Inventory,
    InboundOrder, InboundOrderItem, OutboundOrder,
    OutboundOrderItem, HandlingUnit, DispatchSession,
    StockMovement
)
from .forms import (
    WarehouseForm, ProductForm, InboundOrderForm, InboundOrderItemForm,
    OutboundOrderForm, OutboundOrderItemForm, InventoryForm, StockMovementForm
)

User = get_user_model()

# --- Home & Dashboard ---
def index(request):
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def dashboard_view(request):
    context = {
        'total_warehouses': Warehouse.objects.count(),
        'total_products': Product.objects.count(),
        'total_inventory_items': Inventory.objects.count(),
        'pending_inbound': InboundOrder.objects.filter(status='Pending').count(),
        'pending_outbound': OutboundOrder.objects.filter(status='Pending').count(),
    }
    return render(request, 'partials/dashboard.html', context)


# --- Dispatch Views ---
def scan_hu(request, dispatch_session_id):
    hu_code = request.POST.get("hu_code")
    hu = HandlingUnit.objects.filter(hu_code=hu_code).first()
    if not hu:
        messages.error(request, "Invalid HU code.")
    elif hu.is_scanned:
        messages.warning(request, "HU already scanned.")
    else:
        hu.is_scanned = True
        hu.scanned_at = timezone.now()
        hu.save()
        messages.success(request, f"HU {hu_code} scanned successfully.")
    return redirect('dispatch_session_detail', dispatch_session_id=dispatch_session_id)

def complete_dispatch(request, dispatch_session_id):
    session = get_object_or_404(DispatchSession, id=dispatch_session_id)
    hus = HandlingUnit.objects.filter(outbound_order_item__outbound_order=session.outbound_order)
    all_scanned = hus.filter(is_scanned=True).count() == hus.count()

    if not all_scanned:
        messages.error(request, "Not all HUs are scanned.")
        return redirect('dispatch_session_detail', dispatch_session_id=session.id)

    session.completed_at = timezone.now()
    session.save()
    messages.success(request, "Dispatch completed successfully.")
    return redirect('dashboard')

def dispatch_session_detail(request, dispatch_session_id):
    session = get_object_or_404(DispatchSession, id=dispatch_session_id)
    hus = HandlingUnit.objects.filter(outbound_order_item__outbound_order=session.outbound_order)
    context = {
        'session': session,
        'hus': hus,
        'scanned_count': hus.filter(is_scanned=True).count(),
        'total_count': hus.count(),
    }
    return render(request, 'partials/dispatch_session.html', context)


# --- Warehouse Views ---
class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'partials/warehouse/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural.title()
        context['fields'] = [field.name for field in self.model._meta.fields if field.name != 'id']  # exclude 'id' if needed
        return context


class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'partials/warehouse/form.html'
    success_url = reverse_lazy('warehouse-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = self.model._meta.verbose_name.title()
        return context


# --- Product Views ---
class ProductListView(ListView):
    model = Product
    template_name = 'partials/products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural.title()
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'partials/products/form.html'
    success_url = reverse_lazy('product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = self.model._meta.verbose_name.title()
        return context


# --- Inbound Order Views ---
class InboundOrderListView(ListView):
    model = InboundOrder
    template_name = 'partials/inbound/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural.title()
        return context

class InboundOrderCreateView(CreateView):
    model = InboundOrder
    form_class = InboundOrderForm
    template_name = 'partials/inbound/form.html'
    success_url = reverse_lazy('inbound-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = self.model._meta.verbose_name.title()
        return context


# --- Outbound Order Views ---
class OutboundOrderListView(ListView):
    model = OutboundOrder
    template_name = 'partials/outbound/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural.title()
        return context

class OutboundOrderCreateView(CreateView):
    model = OutboundOrder
    form_class = OutboundOrderForm
    template_name = 'partials/outbound/form.html'
    success_url = reverse_lazy('outbound-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = self.model._meta.verbose_name.title()
        return context


# --- Inventory Views ---
class InventoryListView(ListView):
    model = Inventory
    template_name = 'partials/inventory/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural.title()
        return context


# --- Stock Movement Views ---
class StockMovementListView(ListView):
    model = StockMovement
    template_name = 'partials/movement/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural.title()
        return context

class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'partials/movement/form.html'
    success_url = reverse_lazy('movement-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = self.model._meta.verbose_name.title()
        return context

def generate_handling_units(outbound_item):
    for i in range(outbound_item.quantity_ordered):
        HandlingUnit.objects.create(
            hu_code=f'HU-{outbound_item.id}-{i+1}',
            product=outbound_item.product,
            outbound_order_item=outbound_item,
        )
