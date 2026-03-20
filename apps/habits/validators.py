# apps/habits/validators.py
from rest_framework.serializers import ValidationError


class HabitValidator:
    """Комплексная валидация привычек"""

    def __call__(self, data):
        # 1. Исключить одновременный выбор связанной привычки
        # и указания вознаграждения
        linked_habit = data.get('linked_habit')
        reward = data.get('reward')

        if linked_habit and reward:
            raise ValidationError(
                "Нельзя одновременно указывать связанную привычку и "
                "вознаграждение. Выберите что-то одно."
            )

        # 2. В связанные привычки могут попадать только привычки
        # с признаком приятной привычки
        if linked_habit and not linked_habit.is_pleasant:
            raise ValidationError(
                {"linked_habit": "В связанные привычки могут попадать "
                                 "только приятные привычки"}
            )

        # 3. У приятной привычки не может быть вознаграждения
        # или связанной привычки
        is_pleasant = data.get('is_pleasant')
        if is_pleasant and (linked_habit or reward):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения "
                "или связанной привычки"
            )

        # 4. Время выполнения должно быть не больше 120 секунд
        duration = data.get('duration_sec')
        if duration and duration > 120:
            raise ValidationError(
                {"duration_sec": "Время выполнения должно быть "
                                 "не больше 120 секунд"}
            )

        # 5. Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        periodicity = data.get('periodicity')
        if periodicity and periodicity > 7:
            raise ValidationError(
                {"periodicity": "Нельзя выполнять привычку реже, "
                                "чем 1 раз в 7 дней"}
            )

        return data
