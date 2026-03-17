from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import time
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            owner=self.user,
            place='Дом',
            time=time(9, 0),
            action='Сделать зарядку',
            duration_sec=60,
            periodicity=1
        )

        self.assertEqual(habit.place, 'Дом')
        self.assertEqual(habit.action, 'Сделать зарядку')
        self.assertEqual(habit.owner, self.user)
        self.assertFalse(habit.is_pleasant)
        self.assertFalse(habit.is_public)


class HabitAPITest(APITestCase):
    """Тесты API привычек"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            'place': 'Офис',
            'time': '10:00:00',
            'action': 'Пить воду',
            'duration_sec': 30,
            'periodicity': 1
        }

    def test_create_habit(self):
        """Тест создания привычки через API"""
        response = self.client.post('/api/habits/', self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, 'Пить воду')

    def test_list_my_habits(self):
        """Тест получения списка своих привычек"""
        Habit.objects.create(owner=self.user, **self.habit_data)

        response = self.client.get('/api/habits/my_habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_public_habits_list(self):
        """Тест получения списка публичных привычек"""
        # Создаем публичную привычку другого пользователя
        other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )
        Habit.objects.create(
            owner=other_user,
            place='Парк',
            time=time(18, 0),
            action='Гулять',
            duration_sec=120,
            periodicity=1,
            is_public=True
        )

        # Неаутентифицированный пользователь
        self.client.logout()
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)