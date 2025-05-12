# backend/app/core/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.discovery_service import DiscoveryService

scheduler = AsyncIOScheduler()

# Scheduled job: Refresh symbols every 30 minutes
@scheduler.scheduled_job("interval", minutes=30)
async def refresh_symbols():
    await DiscoveryService.refresh_all_symbols()

# Start the scheduler (must be called explicitly during app startup)
def start_scheduler():
    scheduler.start()
