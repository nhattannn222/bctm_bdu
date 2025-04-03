from celery import shared_task
from django.utils.timezone import now
from .services import TaoBaoCaoTuan

@shared_task
def them_baocao_moi():
    obj = TaoBaoCaoTuan()
    return obj.run()