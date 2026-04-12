"""
Job Scheduler Configuration
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


def start_scheduler():
    """Start the job scheduler"""
    if not scheduler.running:
        scheduler.start()


async def shutdown_scheduler():
    """Shutdown the job scheduler"""
    if scheduler.running:
        scheduler.shutdown()


# TODO: Add scheduled jobs
# @scheduler.scheduled_job('cron', hour=9, minute=0)
# async def daily_report():
#     """Generate daily report"""
#     pass
