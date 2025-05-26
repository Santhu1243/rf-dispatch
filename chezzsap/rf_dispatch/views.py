from django.shortcuts import render
from django.shortcuts import render
from .models import Warehouse, Product, Inventory, InboundOrder, OutboundOrder
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import HandlingUnit, DispatchSession
from django.contrib.auth import get_user_model


User = get_user_model()
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


def scan_hu(request, dispatch_session_id):
    hu_code = request.POST.get("hu_code")
    try:
        hu = HandlingUnit.objects.get(hu_code=hu_code)
        if hu.is_scanned:
            messages.warning(request, "HU already scanned.")
        else:
            hu.is_scanned = True
            hu.scanned_at = timezone.now()
            hu.save()
            messages.success(request, f"HU {hu_code} scanned successfully.")
    except HandlingUnit.DoesNotExist:
        messages.error(request, "Invalid HU code.")
    return redirect('dispatch_session_detail', dispatch_session_id=dispatch_session_id)


def complete_dispatch(request, dispatch_session_id):
    session = get_object_or_404(DispatchSession, id=dispatch_session_id)
    all_scanned = HandlingUnit.objects.filter(
        outbound_order_item__outbound_order=session.outbound_order
    ).count() == HandlingUnit.objects.filter(
        outbound_order_item__outbound_order=session.outbound_order,
        is_scanned=True
    ).count()

    if not all_scanned:
        messages.error(request, "Not all HUs are scanned.")
        return redirect('dispatch_session_detail', dispatch_session_id=session.id)

    session.completed_at = timezone.now()
    session.save()
    messages.success(request, "Dispatch completed successfully.")
    return redirect('dashboard')

from django.shortcuts import render, get_object_or_404
from .models import DispatchSession, HandlingUnit

def dispatch_session_detail(request, dispatch_session_id):
    session = get_object_or_404(DispatchSession, id=dispatch_session_id)
    hus = HandlingUnit.objects.filter(outbound_order_item__outbound_order=session.outbound_order)

    scanned_count = hus.filter(is_scanned=True).count()
    total_count = hus.count()

    context = {
        'session': session,
        'hus': hus,
        'scanned_count': scanned_count,
        'total_count': total_count,
    }
    return render(request, 'partials/dispatch_session.html', context)
