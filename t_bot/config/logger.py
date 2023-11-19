import logging
import os
import sys

from loguru import logger

from config import settings


def init_logging():
    if not settings.LOGS_DIR.is_dir():
        os.mkdir(settings.LOGS_FOLDER)

    logging.basicConfig(
        level=logging.INFO,
        # filename=settings.LOGS_DIR / "log.log",
        format="[%(asctime)s - %(levelname)s] %(name)s - %(message)s",
    )


logger.remove()
loguru_sink = settings.ENV.str("LOGURU_FILE", None)
logger.add(
    sink=settings.LOGS_DIR / loguru_sink if loguru_sink is not None else sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    colorize=not bool(loguru_sink)
)
