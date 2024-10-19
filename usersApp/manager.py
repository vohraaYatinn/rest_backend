
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta

class MenuManager:

    @staticmethod
    def admin_check_login(data):
        username = data.get('userId', False)
        pass