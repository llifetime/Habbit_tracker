from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    """Модель привычки"""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name="Владелец"
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место",
        help_text="Место, где выполняется привычка"
    )
    time = models.TimeField(
        verbose_name="Время",
        help_text="Время выполнения привычки"
    )
    action = models.TextField(
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка"
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка"
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Привычка, которая связана с другой привычкой"
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (в днях)",
        help_text="Периодичность выполнения привычки для напоминания в днях"
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения"
    )
    duration_sec = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение (в секундах)",
        help_text="Время, которое предположительно потратит пользователь"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Привычки можно публиковать в общий доступ"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action[:50]}..."