from rest_framework import serializers

from main.models import Course, Lesson, Payment
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

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платеж"""

    class Meta:
        model = Payment
        fields = '__all__'
