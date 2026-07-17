import asyncio
import sys


def configure_event_loop() -> None:
    """
    Psycopg async does not support the default ProactorEventLoop on Windows.
    Configure SelectorEventLoop only for Windows development.
    """
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )