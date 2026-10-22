import asyncio
import logging
import signal
import sys

from app.core.scheduler import create_scheduler

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("scheduler")


async def main() -> None:
    scheduler = create_scheduler()
    scheduler.start()
    for job in scheduler.get_jobs():
        logger.info("Job registrado: %s (proxima execucao: %s)", job.id, job.next_run_time)

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop.set)
        except NotImplementedError:  # Windows
            pass
    await stop.wait()
    scheduler.shutdown(wait=False)


if __name__ == "__main__":
    asyncio.run(main())
