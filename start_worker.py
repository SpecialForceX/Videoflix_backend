import os
import django
from django_rq.queues import get_queues
from rq import SimpleWorker

# Django Settings setzen
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_hub.settings")
django.setup()

# Queues laden
queues = get_queues()

# Worker starten – ohne Timeout-Mechanismus
worker = SimpleWorker(queues)
worker.work(with_scheduler=True)

