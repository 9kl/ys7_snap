from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers import interval
from apscheduler.triggers.cron import CronTrigger
from pytz import utc

jobstores = {
    'default': MemoryJobStore()
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


def timer(interval_seconds=10):
    def _timer(fn):
        trigger = interval.IntervalTrigger(seconds=interval_seconds)
        scheduler.add_job(fn, trigger=trigger)

    return _timer


def corn(cron_expr):
    def _timer(fn):
        trigger = CronTrigger.from_crontab(cron_expr)
        scheduler.add_job(fn, trigger=trigger)

    return _timer
