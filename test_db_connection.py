# test_db_connection.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connections
from django.db.utils import OperationalError

db_conn = connections['default']
try:
    c = db_conn.cursor()
    print("✅ Подключение к базе данных успешно!")
except OperationalError:
    print("❌ Ошибка подключения к базе данных")