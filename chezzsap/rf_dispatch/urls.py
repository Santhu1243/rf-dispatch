from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dispatch/<int:dispatch_session_id>/', views.dispatch_session_detail, name='dispatch_session_detail'),
    path('dispatch/<int:dispatch_session_id>/scan/', views.scan_hu, name='scan_hu'),
    path('dispatch/<int:dispatch_session_id>/complete/', views.complete_dispatch, name='complete_dispatch'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

