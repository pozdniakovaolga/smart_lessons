from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, DestroyAPIView

from main.models import Course, Lesson
from main.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(CreateAPIView):
    """Контроллер создания урока"""
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра конкретного урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер редактирования урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    """Контроллер удаления урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
