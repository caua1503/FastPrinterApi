from celery.schedules import crontab

from app.core.task import celery_app

celery_app.conf.beat_schedule = {
    "get_all_printers_maintenance_info": {
        "task": "app.core.task.task_get_all_printers_maintenance_info",
        "schedule": crontab(hour="3", minute="0"),
    }
}
