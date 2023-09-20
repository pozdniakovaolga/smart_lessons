from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView

from main.models import Course, Lesson, Payment
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


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


class PaymentListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson', 'method']
