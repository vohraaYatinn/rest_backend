
import sys

sys.path.insert(0, '../../')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_backend.settings')
import django
django.setup()

from django.utils import timezone
import requests
from orders.models import Order, UserCart

pending_orders = Order.objects.filter(payment_status="pending")
url = "https://api.ifthenpay.com/spg/payment/mbway/status"

for orders in pending_orders:
    params = {
        "mbWayKey": "RLA-844371",
        "requestId": orders.payment_reference_number
    }
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()
    if response_json["Message"] != "Pending":
        if response_json["Message"] == "Failed" or response_json["Message"] == "Expired" or response_json["Message"] == "Declined by user":
            orders.payment_status = "failed"
        elif response_json["Message"] == "Success":
            orders.payment_status = "success"
            UserCart.objects.filter(user_id=orders.user_id).delete()


    