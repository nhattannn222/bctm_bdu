import os
from celery import Celery
from celery.schedules import crontab

# Thiết lập mặc định Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_bctm.settings')

app = Celery('backend_bctm')

# Load config từ Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Khai báo lịch trình chạy task tự động
app.conf.beat_schedule = {
    'run-every-friday-8am': {
        'task': 'api.tasks.them_baocao_moi',  # Thay đổi theo tên task thực tế của bạn
        'schedule': crontab(hour=8, minute=0, day_of_week=5),  # Chạy 8h sáng thứ 6
    },
}

# Tự động tìm kiếm các task trong ứng dụng Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')