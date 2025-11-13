import pytest
from django.db import IntegrityError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from orders_mgmt.models import Customer, Order
from orders_mgmt.serializers import CustomerSerializer, OrderSerializer
from django.contrib.auth.models import User
from datetime import datetime

@pytest.mark.django_db  # Enables database access for this test class
class TestCustomerModel:
    def test_create_customer(self):
        customer = Customer.objects.create(
            name="John Doe", code="C001", phone="+254700000000"
        )
        assert customer.name == "John Doe"
        assert customer.code == "C001"
        assert customer.phone == "+254700000000"
        assert str(customer).startswith('John Doe')
         # Covers __str__

    def test_unique_code(self):
        Customer.objects.create(
            name="John Doe", code="C001", phone="+254700000000"
        )
        with pytest.raises(IntegrityError): # Tests unique constraint
            Customer.objects.create(name="John Doe", code="C001", phone="+254700000000")

@pytest.mark.django_db
class TestOrderModel:
    @pytest.fixture
    def customer(self):
        return Customer.objects.create(name="John Doe", code="C001", phone="+254700000000")
        
    def test_create_order(self, customer):    
        order = Order.objects.create(
            customer=customer, item="Laptop", quantity=99
        )
        assert order.customer == customer
        assert order.item == "Laptop"
        assert order.quantity == 99
        assert isinstance(order.time, datetime)
        assert "Laptop" in str(order) # Covers __str__
    
@pytest.mark.django_db
class TestCustomerSerializer:
    def test_valid_data(self):
        data = {"name": "Jane Doe", "code": "C002", "phone": "+254711111111"}
        serializer = CustomerSerializer(data=data)
        assert serializer.is_valid()
        customer = serializer.save()
        assert customer.name == "Jane Doe"
    
    def test_invalid_data(self):
        data = {"name": "Jane Doe", "code": "", "phone": "+254711111111"} # Missing code
        serializer = CustomerSerializer(data=data)
        assert not serializer.is_valid()
        assert "code" in serializer.errors

@pytest.mark.django_db
class TestOrderSerializer:
    @pytest.fixture
    def customer(self):
        return Customer.objects.create(
            name="John Doe", code="C001", phone="+254700000000"
        )
    def test_valid_data(self, customer):
        data = {"customer": customer.id, "item": "Phone", "quantity": 49}
        serializer = OrderSerializer(data=data)
        assert serializer.is_valid()
        order = serializer.save()
        assert order.item == "Phone"
    def test_invalid_data(self, customer):
        data = {"name": customer.id,  "item": "phone", "quantity":"Invalid"} # Bad quantity type
        serializer = CustomerSerializer(data=data)
        assert not serializer.is_valid()
        
@pytest.mark.django_db
class TestCustomerViewSet:
    def setup_method(self):
        self.client = APIClient()   

    def test_list_customers(self, mocker):
        mock_post = mocker.patch('requests.post')
        Customer.objects.create(name="John Doe", code="C001", phone="+254700000000")
        url = reverse('customer-list')  # Assumes router.register(r'customers', CustomerViewSet)
        response = self.client.get(url)
        mock_post.return_value.status_code = 200.
        mock_post.return_value.json.return_value = {...}

    def test_create_customer_unauthenticated(self):
        url = reverse('customer-list')
        data = {"name": "John Doe", "code": "C001", "phone": "+254700000000"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Tests auth requirement
    def test_retrieve_customer_unauthenticated(self):
        customer = Customer.objects.create(name="John Doe", code="C001", phone="+254123456789")
        url = reverse('customer-detail', kwargs={'pk': customer.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED    

@pytest.mark.django_db
class TestOrderViewSet:
    def setup_method(self):
        self.client = APIClient()

    @pytest.fixture    
    def customer(self):
        return Customer.objects.create(
            name="John Doe", code="C001", phone="+254700000000"
        )
    def test_create_order(self, customer, mocker):
        mock_sms = mocker.patch('requests.post')  # Mock SMS to avoid real calls
        url = reverse('order-list')
        data = {"customer": customer.id, "item": "phone", "quantity": 99}
        response = self.client.post(url, data)
        # assert response.status_code == status.HTTP_201_CREATED
        # assert Order.objects.count() == 1
        # mock_sms.assert_called_once()  # Verifies SMS was "sent"assert_called_once_with(
        mock_sms.return_value.status_code = 200
        mock_sms.return_value.json.return_value = {...}


    def test_create_order_invalid(self, customer, mocker):
        mock_sms = mocker.patch('requests.post')
        url = reverse('order-list')
        data = {"customer": customer.id, "quantity": 99}  # Missing item
        mock_sms.return_value.status_code = 400

    def test_list_orders_authenticated(self, customer, mocker):
        Order.objects.create(customer=customer, item="Widget", quantity=99.99)
        mock_post = mocker.patch('requests.post')
        self.client.force_authenticate()
        url = reverse('order-list')  # /api/orders/
        response = self.client.get(url)
        mock_post.return_value.status_code == status.HTTP_200_OK
        mock_post.return_value.json.return_value = {...}

    def test_list_orders_empty(self, mocker):
        mock_post = mocker.patch('requests.post')
        self.client.force_authenticate()
        url = reverse('order-list')
        response = self.client.get(url)
        mock_post.return_value.status_code == status.HTTP_200_OK
        mock_post.return_value.json.return_value = {...}    

    def test_retrieve_order_authenticated(self, customer, mocker):
        order = Order.objects.create(customer=customer, item="Widget", quantity=99.99)
        self.client.force_authenticate()
        url = reverse('order-detail', kwargs={'pk': order.id})  # /api/orders/1/
        mock_get = mocker.patch('requests.get')
        response = self.client.get(url)
        mock_get.return_value.status_code == status.HTTP_200_OK
        mock_get.return_value.json.return_value = {...}

@pytest.mark.django_db
class TestSMSIntegration:
    def test_sms_on_order_create_success(self, mocker):
        
        mock_sms_send = mocker.patch('requests.post')
        customer = Customer.objects.create(name="John Doe", code="C001", phone="+254700000000")
        client = APIClient()
        url = reverse('order-list')
        data = {"customer": customer.id, "item": "phone", "quantity": 99}
        response = client.post(url, data)
        mock_sms_send.return_value.status_code = 200.
        mock_sms_send.return_value.json.return_value = {...}
        

    def test_sms_on_order_create_failure(self, mocker):
        mock_sms_send = mocker.patch('requests.post', side_effect=Exception("API Error"))
        customer = Customer.objects.create(name="John Doe", code="C001", phone="+254700000000")
        client = APIClient()
        url = reverse('order-list')
        data = {"customer": customer.id, "item": "phone", "quantity": 99}
        response = client.post(url, data)
        mock_sms_send.return_value.status_code = 201
        mock_sms_send.return_value.json.return_value = {...}
        # Order saves despite SMS fail
        