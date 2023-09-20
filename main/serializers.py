from rest_framework import serializers

from main.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курс"""
    lesson_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count']

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урок"""

    class Meta:
        model = Lesson
        fields = '__all__'
