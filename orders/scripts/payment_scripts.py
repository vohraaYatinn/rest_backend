
import sys
from django.utils import timezone

sys.path.insert(0, '../../')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_backend.settings')
import django
django.setup()

from orders.models import Order
today = timezone.now().date()

pending_orders = order.objects.filter(payment_status="pending")

for orders in pending_orders:
    