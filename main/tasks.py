from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from main.models import Subscription

@shared_task
def send_mail_by_subscription(course_pk):
    for subscription in Subscription.objects.filter(course_id=course_pk):
        try:
            send_mail(
                subject='Обновление материалов курса',
                message=f'Обновился курс, на который вы подписаны',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email]
            )
        except Exception as expt:
            return expt
