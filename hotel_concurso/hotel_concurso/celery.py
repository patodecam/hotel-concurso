from __future__ import absolute_import,unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_concurso.settings")
app = Celery("hotel_concurso")


app.conf.enable_utc=False
app.conf.update(timezone='America/Santiago')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

#celery beat settings
app.conf.beat_schedule={

}