# apps/habits/services.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramService:
    """Сервис для работы с Telegram API"""

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id, text):
        """Отправка сообщения пользователю"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
            return None

    def send_habit_reminder(self, user, habit):
        """Отправка напоминания о привычке"""
        message = f"""
🔔 <b>Напоминание о привычке!</b>

📍 <b>Место:</b> {habit.place}
⏰ <b>Время:</b> {habit.time.strftime('%H:%M')}
📝 <b>Действие:</b> {habit.action}
⏱ <b>Длительность:</b> {habit.duration_sec} сек.
"""
        if habit.reward:
            message += f"🎁 <b>Вознаграждение:</b> {habit.reward}"
        elif habit.linked_habit:
            linked_action = habit.linked_habit.action
            message += f"🎯 <b>После выполнения:</b> {linked_action}"

        return self.send_message(user.telegram_chat_id, message)
