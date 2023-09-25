from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from main.models import Course, Lesson, Payment
from main.permissions import CoursePermissions, IsModerator, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, CoursePermissions]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.created_by = self.request.user
        new_course.save()

    def list(self, request):
        if self.request.user.is_moderator:
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(created_by=self.request.user)
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonCreateAPIView(CreateAPIView):
    """Контроллер создания урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.created_by = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_moderator:
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.filter(created_by=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра конкретного урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер редактирования урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    """Контроллер удаления урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson', 'method']
    permission_classes = [IsAuthenticated]
