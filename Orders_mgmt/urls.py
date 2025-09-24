from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
# router.register(r'index', IndexViewSet, basename='index')
urlpatterns = [
    path('', include(router.urls)), 
]
    