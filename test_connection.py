# test_connection.py
from django.db import connection
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Подключение успешно!")
        cursor.execute("SELECT current_user")
        user = cursor.fetchone()
        print(f"👤 Текущий пользователь: {user[0]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
