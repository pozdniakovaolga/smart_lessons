from users.models import User
from datetime import datetime, timedelta, timezone
from celery import shared_task

@shared_task
def check_last_login():
    """Деактивирует пользователей, которые не входили в приложение больше 30 дней (проверка 1 раз в день)"""
    for user in User.objects.filter(is_active=True):
        if user.last_login:
            if datetime.now(timezone.utc) - timedelta(days=30) > user.last_login:
                user.is_active = False
                user.save()
