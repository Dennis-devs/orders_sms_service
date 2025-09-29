
"URL config for Python_service project."

from django.contrib import admin
from django.urls import path, include
from Orders_mgmt.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Orders_mgmt.urls')),
    path('', index, name='index'),
    path('oidc/', include('mozilla_django_oidc.urls')),

]
