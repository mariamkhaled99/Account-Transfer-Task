from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('accounts/', views.list_accounts, name='list_accounts'),
    path('transfer/', views.transfer_funds, name='transfer_funds'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('', views.home, name='home'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)