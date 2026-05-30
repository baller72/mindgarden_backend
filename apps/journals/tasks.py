from celery import shared_task
from .services import process_journal_entry as _process

@shared_task
def process_journal_entry_task(entry_id: int):
    _process(entry_id)