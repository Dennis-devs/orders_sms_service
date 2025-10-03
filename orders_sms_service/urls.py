
# URL config for Python_service project.

from django.contrib import admin
from django.urls import path, include
from orders_mgmt.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders_mgmt.urls')),
    path('', index, name='index'),
    path('oidc/', include('mozilla_django_oidc.urls')),
]
