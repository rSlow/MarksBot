from pathlib import Path

import pytz

import utils.groups
from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent
ENV = get_env(env_file=BASE_DIR.parent / ".env")
TEMPLATES_DIR = BASE_DIR / "jinja"

TIMEZONE = pytz.timezone(ENV.str("TIMEZONE", "Asia/Vladivostok"))
ADMINS: list[int] = ENV.list("ADMINS")
GROUPS: list[str] = ENV.list("GROUPS")
COURSES: list[int] = utils.groups.form_courses(GROUPS)
API_KEY: str = ENV.str("API_KEY")
TABLE_ID: str = ENV.str("TABLE_ID")

LOGS_FOLDER = "logs"
LOGS_DIR = BASE_DIR / LOGS_FOLDER
