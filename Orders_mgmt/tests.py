import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from unittest.mock import patch
from django.contrib.auth.models import User
from datetime import datetime


# Create your tests here.
@pytest.mark.django_db
def test_customer_model():
    customer = Customer.objects.create(
        name="John Doe", code="C001", phone="+254700000000"
    )
    assert customer.name == "John Doe"
    assert customer.code == "C001"
    assert customer.phone == "+254700000000"
    assert str(customer) == "John Doe"

@pytest.mark.django_db
def test_order_model():
    customer = Customer.objects.create(
        name="John Doe", code="C001", phone="+254700000000"
    )
    order = Order.objects.create(
        customer=customer, item="Laptop", quantity=999.99
    )
    assert order.customer == customer
    assert order.item == "Laptop"
    assert order.quantity == 999.99
    assert isinstance(order.time, datetime)
    assert str(order) == "Laptop for John Doe"

@pytest.mark.django_db
def test_customer_serializer():
    data = {"name": "Jane Doe", "code": "C002", "phone": "+254711111111"}
    serializer = CustomerSerializer(data=data)
    assert serializer.is_valid()
    customer = serializer.save()
    assert customer.name == "Jane Doe"
    assert customer.code == "C002"
    assert customer.phone == "+254711111111"

    # Test invalid phone
    data = {"name": "Jane Doe", "code": "C003", "phone": "123"}
    serializer = CustomerSerializer(data=data)
    assert not serializer.is_valid()
    assert "phone" in serializer.errors   

@pytest.mark.django_db
def test_order_serializer():
    customer = Customer.objects.create(
        name="John Doe", code="C001", phone="+254700000000"
    )
    data = {"customer": customer.id, "item": "Phone", "quantity": 499.99}
    serializer = OrderSerializer(data=data)
    assert serializer.is_valid()
    order = serializer.save()
    assert order.customer == customer
    assert order.item == "Phone"
    assert order.quantity == 499.99

@pytest.mark.django_db
def test_customer_viewset_create():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    client.force_authenticate(user=user)
    data = {"name": "John Doe", "code": "C001", "phone": "+254700000000"}
    response = client.post(reverse("customer-list"), data, format="json")
    assert response.status_code == 201
    assert Customer.objects.count() == 1
    assert Customer.objects.first().name == "John Doe"    

@pytest.mark.django_db
def test_order_viewset_create_with_sms():
    customer = Customer.objects.create(
        name="John Doe", code="C001", phone="+254700000000"
    )
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()
    client.force_authenticate(user=user)
    data = {"customer": customer.id, "item": "Laptop", "quantity": 999.99}
    with patch("core.sms_service.SMSService.send_sms") as mock_sms:
        mock_sms.return_value = {"SMSMessageData": {"Recipients": [{"status": "Success"}]}}
        response = client.post(reverse("order-list"), data, format="json")
        assert response.status_code == 201
        assert Order.objects.count() == 1
        assert Order.objects.first().item == "Laptop"
        mock_sms.assert_called_once_with(
            f"Your order for Laptop (quantity: 999.99, Time: {Order.objects.first().time}) has been placed.",
            [customer.phone],
            sender_id="AFRICASTKNG"
        )

@pytest.mark.django_db
def test_order_viewset_sms_failure():
    customer = Customer.objects.create(
        name="John Doe", code="C001", phone="+254700000000"
    )
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()
    client.force_authenticate(user=user)
    data = {"customer": customer.id, "item": "Laptop", "quantity": 999.99}
    with patch("core.sms_service.SMSService.send_sms") as mock_sms:
        mock_sms.side_effect = Exception("Sandbox unavailable")
        response = client.post(reverse("order-list"), data, format="json")
        assert response.status_code == 201  # Order still created
        assert Order.objects.count() == 1
        mock_sms.assert_called_once()        