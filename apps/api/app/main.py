from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.auth.bootstrap import ensure_bootstrap_admin
from app.core.config import settings
from app.core.event_loop import configure_event_loop
from app.core.logging import configure_logging
from app.services.news_scheduler import NewsRefreshScheduler

configure_event_loop()
configure_logging()

@asynccontextmanager
async def lifespan(_: FastAPI):
    await ensure_bootstrap_admin()
    scheduler = None
    if settings.NEWS_SCHEDULER_ENABLED:
        scheduler = NewsRefreshScheduler(settings.NEWS_REFRESH_INTERVAL_MINUTES * 60)
        scheduler.start()
    yield
    if scheduler is not None:
        await scheduler.stop()


app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

if __name__ == "__main__":
    # `uvicorn.run()` (and the `uvicorn app.main:app` CLI form) resets the
    # event loop policy itself via Server.run() before calling asyncio.run(),
    # which clobbers configure_event_loop() above. Driving Server.serve()
    # directly on a loop we create ourselves is the only way the Windows
    # SelectorEventLoop policy actually sticks for psycopg's async driver.
    import asyncio
    import os

    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    server = uvicorn.Server(config)

    configure_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.serve())
