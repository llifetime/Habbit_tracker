import os
from celery import Celery

# Установка модуля настроек Django по умолчанию для программы 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('habit_tracker')

# Использование строки конфигурации означает, что объекту Celery не нужно сериализовать
# объект конфигурации. Вместо этого передается пространство имен с заглавными буквами.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка модулей задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
