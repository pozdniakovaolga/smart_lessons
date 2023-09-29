from rest_framework import serializers

from main.models import Course, Lesson, Payment, Subscription
from main.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урок"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курс"""
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

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


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Подписка"""

    class Meta:
        model = Subscription
        fields = '__all__'
