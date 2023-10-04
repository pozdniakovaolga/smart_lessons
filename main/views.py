import os

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from main.models import Course, Lesson, Payment, Subscription
from main.paginators import PagePagination
from main.permissions import CoursePermissions, IsModerator, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentRetrieveSerializer, PaymentSuccessSerializer
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = PagePagination
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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
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
    pagination_class = PagePagination
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


class PaymentCreateAPIView(CreateAPIView):
    """Контроллер создания платежа"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра конкретного платежа"""
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentSuccessAPIView(generics.RetrieveAPIView):
    """Контроллер успешного платежа"""
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    serializer_class = PaymentSuccessSerializer
    queryset = Payment.objects.all()

    def get_object(self):

        session_id = self.request.query_params.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        payment_id = session.metadata['payment_id']
        obj = get_object_or_404(self.get_queryset(), pk=payment_id)

        if not obj.is_paid:
            if session.payment_status == 'paid':
                obj.is_paid = True
                obj.save()
        return obj


class SubscriptionCreateAPIView(CreateAPIView):
    """Контроллер установки подписки пользователя"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(DestroyAPIView):
    """Контроллер удаления подписки у пользователя"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
