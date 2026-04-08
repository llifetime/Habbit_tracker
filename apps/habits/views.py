# apps/habits/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Habit
from .serializers import HabitSerializer, HabitPublicSerializer
from .paginations import HabitPagination
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_permissions(self):
        """Определяем права доступа для разных действий"""
        if self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        elif self.action == 'public':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Получение queryset в зависимости от действия"""
        if self.action == 'public':
            return Habit.objects.filter(is_public=True)

        return Habit.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'public':
            return HabitPublicSerializer
        return HabitSerializer

    def perform_create(self, serializer):
        """Сохранение владельца при создании"""
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my_habits(self, request):
        """Список привычек текущего пользователя"""
        habits = self.get_queryset()
        page = self.paginate_queryset(habits)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Список публичных привычек"""
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)

        if page is not None:
            serializer = HabitPublicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HabitPublicSerializer(public_habits, many=True)
        return Response(serializer.data)
