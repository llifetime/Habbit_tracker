# apps/habits/serializers.py
from rest_framework import serializers
from .models import Habit
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'owner', 'owner_username', 'place', 'time', 'action',
            'is_pleasant', 'linked_habit', 'periodicity', 'reward',
            'duration_sec', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_linked_habit(self, value):
        """Дополнительная проверка связанной привычки"""
        if value and value.owner != self.context['request'].user:
            raise serializers.ValidationError("Можно связывать только свои привычки")
        return value

    def validate(self, attrs):
        # Применяем кастомный валидатор
        validator = HabitValidator()
        validator(attrs)
        return attrs


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек (только чтение)"""

    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'owner_username', 'place', 'time', 'action',
            'is_pleasant', 'periodicity', 'duration_sec', 'created_at'
        ]
        # read_only_fields должно быть списком или кортежем
        read_only_fields = ['id', 'owner_username', 'place', 'time', 'action',
                            'is_pleasant', 'periodicity', 'duration_sec', 'created_at']