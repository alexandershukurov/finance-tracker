from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from finance.views import index, add_entry
from finance.views import index, add_entry, manage_view, delete_entry

urlpatterns = [
    path('', index, name='index'),
    path('add/', add_entry, name='add_entry'),
    path('manage/', manage_view, name='manage'),
    path('api/', include('finance.urls')),
    path('admin/', admin.site.urls),
]

