from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders_mgmt.models import Customer, Order
from orders_mgmt.serializers import CustomerSerializer, OrderSerializer
import africastalking as africastalking
import os
import requests

# View instantiates the serializer class, passing the parsed(incoming JSON to python datatype e.g dictionary) data from the request to it.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated]   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        # validation checks
        serializer.is_valid(raise_exception=True)
        # If valid: The serializer's validated_data attribute is populated with the clean, validated Python data. view also saves the new order instance to the database by triggering perform_create or create() method.
        self.perform_create(serializer)
        order = serializer.instance
        customer = order.customer

        customer_phone = customer.phone

        message = f"Hello {customer.name}, your order for {order.quantity} of {order.item} at {order.time} has been placed."

        username = "sandbox"
        api_key = os.getenv('AFRICASTALKING_API_KEY')
        url = os.getenv('MESSAGING_URL')

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'apiKey': api_key
        }

        data = {
            'username': username,
            'to': customer_phone,
            'message': message
        }

        try:
            # send response to africastalking gateway
            response = requests.post(url, headers=headers, data=data)
            response_data = response.json()
        # Serializer serializes saved Python object back into a native Python dictionary. DRF's renderer classes then convert this dictionary into a JSON response.
            return Response(response_data, status=201)
        # error handling    
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
   
def index(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {'user': request.user})
    else:
        return render(request, 'login.html')

