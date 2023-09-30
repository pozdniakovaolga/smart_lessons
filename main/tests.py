import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import Lesson, Course, Subscription
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class LessonTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:

        self.user = User.objects.create(
            email='user@test.ru',
            password='test_asdfg',
            phone='007',
            city='LA')

        self.moderator = User.objects.create(
            email='moderator@test.ru',
            password='moderator_asdfg',
            phone='008',
            city='NY',
            is_moderator=True)

        self.course = Course.objects.create(
            title='test_course',
            description='test_course',
            created_by=self.user
        )
        self.lesson = Lesson.objects.create(
            title='test_lesson',
            course=self.course,
            description='test_lesson',
            link='https://www.youtube.com/watch?v=34Rp6KVGIEM',
            created_by=self.user
        )
        self.lesson_2 = Lesson.objects.create(
            title='test_lesson_2',
            course=self.course,
            description='test_lesson_2',
            link='https://www.youtube.com/watch?v=34Rp6KVGIEM',
            created_by=None
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

    def test_getting_lesson_list(self):
        """Тестирование вывода списка уроков для пользователя"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        response = self.client.get(reverse('main:lesson_list'), {}, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            json.loads(response.content)['results'],
            [
                {
                    'id': self.lesson.id,
                    'title': self.lesson.title,
                    'description': self.lesson.description,
                    'preview':  self.lesson.preview,
                    'link': self.lesson.link,
                    'course': self.lesson.course_id,
                    'created_by': self.lesson.created_by_id
                }
            ]
        )

    def test_getting_lesson_list_by_moderator(self):
        """Тестирование вывода списка уроков для модератора"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.moderator).access_token)  # авторизация
        response = self.client.get(reverse('main:lesson_list'), {}, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            json.loads(response.content)['results'],
            [
                {
                    'id': self.lesson.id,
                    'title': self.lesson.title,
                    'description': self.lesson.description,
                    'preview':  self.lesson.preview,
                    'link': self.lesson.link,
                    'course': self.lesson.course_id,
                    'created_by': self.lesson.created_by_id
                },
                {
                    'id': self.lesson_2.id,
                    'title': self.lesson_2.title,
                    'description': self.lesson_2.description,
                    'preview': self.lesson_2.preview,
                    'link': self.lesson_2.link,
                    'course': self.lesson_2.course_id,
                    'created_by': self.lesson_2.created_by_id
                }
            ]
        )

    def test_getting_lesson_list_by_not_authenticated_user(self):
        """Тестирование вывода списка уроков для неавторизованного пользователя"""
        response = self.client.get(reverse('main:lesson_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_getting_lesson(self):
        """Тестирование вывода урока для пользователя"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        response = self.client.get(reverse('main:lesson_get', args=(self.lesson.pk,)), HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            json.loads(response.content),
            {
                'id': self.lesson.id,
                'title': self.lesson.title,
                'description': self.lesson.description,
                'preview': self.lesson.preview,
                'link': self.lesson.link,
                'course': self.lesson.course_id,
                'created_by': self.lesson.created_by_id
            }
        )

    def test_getting_lesson_by_moderator(self):
        """Тестирование вывода урока для модератора"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.moderator).access_token)  # авторизация
        response = self.client.get(reverse('main:lesson_get', args=(self.lesson.pk,)), HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            json.loads(response.content),
            {
                'id': self.lesson.id,
                'title': self.lesson.title,
                'description': self.lesson.description,
                'preview': self.lesson.preview,
                'link': self.lesson.link,
                'course': self.lesson.course_id,
                'created_by': self.lesson.created_by_id
            }
        )

    def test_getting_lesson_by_not_authenticated_user(self):
        """Тестирование вывода урока для модератора"""
        response = self.client.get(reverse('main:lesson_get', args=(self.lesson.pk,)))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_create_lesson(self):
        """Тестирование создания уроков: пользователь"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        data = {
            'title': 'test_lesson_creation',
            'course': self.course.pk,
            'description': 'test_lesson_creation',
            'link': 'https://www.youtube.com/watch?v=34Rp6KVGIEM',
        }

        response = self.client.post(reverse('main:lesson_create'), data, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            3,
            Lesson.objects.all().count()
        )

    def test_create_lesson_by_moderator(self):
        """Тестирование создания уроков: модератор"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.moderator).access_token)  # авторизация
        data = {
            'title': 'test_lesson_creation',
            'course': self.course.pk,
            'description': 'test_lesson_creation',
            'link': 'https://www.youtube.com/watch?v=34Rp6KVGIEM',
        }

        response = self.client.post(reverse('main:lesson_create'), data, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            2,
            Lesson.objects.all().count()
        )

    def test_create_lesson_by_not_authenticated_user(self):
        """Тестирование создания уроков: неавторизованный пользователь"""
        data = {
            'title': 'test_lesson_creation',
            'course': self.course.pk,
            'description': 'test_lesson_creation',
            'link': 'https://www.youtube.com/watch?v=34Rp6KVGIEM',
        }

        response = self.client.post(reverse('main:lesson_create'), data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            2,
            Lesson.objects.all().count()
        )

    def test_update_lesson(self):
        """Тестирование изменения урока: пользователь"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        data = {
            'title': 'test_lesson_update',
            'course': self.course.pk,
            'description': 'test_lesson_update',
            'link': 'https://www.youtube.com/watch?v=34Rp6KVGIEM',
        }

        response = self.client.put(reverse('main:lesson_update', args=[self.lesson.pk]), data, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.lesson.refresh_from_db()

        self.assertEqual(
            self.lesson.title,
            data['title']
        )

    def test_update_lesson_by_moderator(self):
        """Тестирование изменения урока: модератор"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.moderator).access_token)  # авторизация
        data = {
            'title': 'test_lesson_update',
            'course': self.course.pk,
            'description': 'test_lesson_update',
            'link': 'https://www.youtube.com/watch?v=34Rp6KVGIEM',
        }

        response = self.client.put(reverse('main:lesson_update', args=[self.lesson.pk]), data, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.lesson.refresh_from_db()

        self.assertEqual(
            self.lesson.title,
            data['title']
        )

    def test_update_lesson_by_not_authenticated_user(self):
        """Тестирование изменения урока: неавторизованный пользователь"""
        data = {
            'title': 'test_lesson_update',
            'course': self.course.pk,
            'description': 'test_lesson_update',
            'link': 'https://www.youtube.com/watch?v=34Rp6KVGIEM',
        }

        response = self.client.put(reverse('main:lesson_update', args=[self.lesson.pk]), data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока: пользователь"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        response = self.client.delete(reverse('main:lesson_delete', args=[self.lesson.pk]), HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            1,
            Lesson.objects.all().count()
        )

    def test_delete_lesson_by_moderator(self):
        """Тестирование удаления урока: модератор"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.moderator).access_token)  # авторизация
        response = self.client.delete(reverse('main:lesson_delete', args=[self.lesson.pk]), HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            2,
            Lesson.objects.all().count()
        )

    def test_delete_lesson_by_not_authenticated_user(self):
        """Тестирование удаления урока: неавторизованный пользователь"""
        response = self.client.delete(reverse('main:lesson_delete', args=[self.lesson.pk]))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            2,
            Lesson.objects.all().count()
        )

    def test_create_subscription(self):
        """Тестирование создания подписки на курс"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
        }

        response = self.client.post(reverse('main:subscription_create'), data, HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            2,
            Subscription.objects.all().count()
        )

    def test_delete_subscription(self):
        """Тестирование удаления подписки на курс"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        response = self.client.delete(reverse('main:subscription_delete', args=[self.subscription.pk]), HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            0,
            Subscription.objects.all().count()
        )

    def test_subscription_field(self):
        """Тестирование вывода признака подписки на обновления курса при просмотре курса"""
        tkn = 'Bearer ' + str(RefreshToken.for_user(self.user).access_token)  # авторизация
        response = self.client.get(reverse('main:courses-detail', args=(self.course.pk,)), HTTP_AUTHORIZATION=tkn)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.MaxDiff = None
        self.assertEqual(
            json.loads(response.content)['is_subscribed'],
            True
        )
