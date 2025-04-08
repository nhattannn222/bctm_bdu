from apscheduler.schedulers.background import BackgroundScheduler
from .services import tao_bao_cao_tuan, cap_nhat_bao_cao_qua_han

def start():
    scheduler = BackgroundScheduler(timezone="Asia/Ho_Chi_Minh")
    scheduler.add_job(tao_bao_cao_tuan, 'cron', day_of_week='fri', hour=8, minute=0)
    scheduler.add_job(cap_nhat_bao_cao_qua_han, 'cron', day_of_week='fri', hour=22, minute=1)
    scheduler.start()
