from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated]   


def index(request):
    if request.user.is_authenticated:
        return render(request, 'session.html', {'user': request.user})
    else:
        return render(request, 'login.html')

# class IndexViewSet(viewsets.ViewSet):
    
#     renderer_classes = [TemplateHTMLRenderer]
# template_name = 'index.html'


#     permission_classes = [IsAuthenticated]
#     def list(self, request):

#         # context = {
#         #     'user': request.user.is_authenticated
#         # }
        
#         return render(request, self.template_name)
# def home(request):
#     # context = {
#     #     'user': request.user.is_authenticated
#     # }
    
#     return render(request, 'index.html')
    