from celery import shared_task
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, timedelta
import logging

from .models import Habit
from .services import TelegramService
from apps.users.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminders():
    """
    Отправка напоминаний о привычках.
    Запускается каждую минуту по расписанию Celery Beat.
    """
    logger.info("Запуск задачи отправки напоминаний")

    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    # Получаем все привычки, которые нужно выполнить в текущее время
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('owner')

    sent_count = 0
    for habit in habits:
        # Проверяем, нужно ли отправлять напоминание сегодня
        # (учитывая периодичность в днях)
        if should_send_today(habit, current_date):
            # Проверяем, есть ли у пользователя Telegram
            if habit.owner.telegram_chat_id and habit.owner.is_telegram_verified:
                # Проверяем кэш, чтобы не отправить дубликат
                cache_key = f"reminder_sent_{habit.id}_{current_date}"
                if not cache.get(cache_key):
                    service = TelegramService()
                    result = service.send_habit_reminder(habit.owner, habit)

                    if result and result.get('ok'):
                        # Ставим отметку в кэш на 24 часа
                        cache.set(cache_key, True, 60 * 60 * 24)
                        sent_count += 1
                        logger.info(f"Напоминание отправлено для привычки {habit.id}")

    logger.info(f"Задача завершена. Отправлено напоминаний: {sent_count}")
    return f"Sent {sent_count} reminders"


def should_send_today(habit, current_date):
    """
    Проверка, нужно ли отправлять напоминание сегодня
    с учетом периодичности привычки
    """
    # Получаем дату создания привычки
    created_date = habit.created_at.date()

    # Вычисляем разницу в днях
    days_diff = (current_date - created_date).days

    # Если периодичность 1 (ежедневно) - отправляем всегда
    if habit.periodicity == 1:
        return True

    # Для других периодичностей проверяем по модулю
    return days_diff % habit.periodicity == 0