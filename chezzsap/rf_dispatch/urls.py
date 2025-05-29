from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dispatch/<int:dispatch_session_id>/', views.dispatch_session_detail, name='dispatch_session_detail'),
    path('dispatch/<int:dispatch_session_id>/scan/', views.scan_hu, name='scan_hu'),
    path('dispatch/<int:dispatch_session_id>/complete/', views.complete_dispatch, name='complete_dispatch'),
    path('warehouses/', WarehouseListView.as_view(), name='warehouse-list'),
    path('warehouses/create/', WarehouseCreateView.as_view(), name='warehouse-create'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),

    path('inbound/', InboundOrderListView.as_view(), name='inbound-list'),
    path('inbound/create/', InboundOrderCreateView.as_view(), name='inbound-create'),

    path('outbound/', OutboundOrderListView.as_view(), name='outbound-list'),
    path('outbound/create/', OutboundOrderCreateView.as_view(), name='outbound-create'),

    path('inventory/', InventoryListView.as_view(), name='inventory-list'),

    path('movement/', StockMovementListView.as_view(), name='movement-list'),
    path('movement/create/', StockMovementCreateView.as_view(), name='movement-create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

