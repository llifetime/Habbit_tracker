# test_psycopg2.py
try:
    import psycopg2

    print("✅ psycopg2 успешно импортирован")
    print(f"Версия: {psycopg2.__version__}")
except Exception as e:
    print(f"❌ Ошибка импорта psycopg2: {e}")

    # Попробуем найти проблему
    import sys

    print(f"Python path: {sys.path}")

    import os

    print(f"PATH: {os.environ.get('PATH', '')}")