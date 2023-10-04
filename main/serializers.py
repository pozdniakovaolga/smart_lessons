from rest_framework import serializers

from main.models import Course, Lesson, Payment, Subscription
from main.validators import LinkValidator

import stripe
import os


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урок"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курс"""
    lesson_count = serializers.SerializerMethodField(read_only=True)   # количество уроков
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)  # список уроков
    is_subscribed = serializers.SerializerMethodField(read_only=True)  # признак подписки

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons', 'is_subscribed']

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    def get_is_subscribed(self, instance):
        if Subscription.objects.filter(course=instance).count() == 0:
            return False
        else:
            return True


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платеж"""

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения отдельного платежа"""
    link_to_pay = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    @staticmethod
    def get_link_to_pay(instance):  # создание ссылки для оплаты через stripe
        # создание stripe сессии
        stripe.api_key = os.getenv('STRIPE_API_KEY')

        if instance.course:  # при оплате курса
            product_name = instance.course.title
            product_description = instance.course.description
        else:  # при оплате урока
            product_name = instance.lesson.title
            product_description = instance.lesson.description

        product = stripe.Product.create(name=product_name, description=product_description)
        product_price = stripe.Price.create(unit_amount=instance.amount*100, currency="rub", product=product['id'])
        # в success_url передается session_id, в metadata: payment_id
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/payment/success/?succcess=true&session_id={CHECKOUT_SESSION_ID}",
            line_items=[{"price": product_price['id'], "quantity": 1}],
            mode="payment",
            metadata={'payment_id': instance.id},
        )

        return session['url']


class PaymentSuccessSerializer(serializers.ModelSerializer):
    """Сериализатор для успешного платежа"""

    class Meta:
        model = Payment
        fields = ['amount', 'is_paid']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Подписка"""

    class Meta:
        model = Subscription
        fields = '__all__'
