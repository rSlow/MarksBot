from io import BytesIO

from aiogram import Bot

from ORM.marks.practice import PracticeMark
from ORM.marks.study import StudyMark
from ORM.schemas import SStudyMarkOut
from config import settings
from utils.downloader import GoogleExcelDownloader
from utils.excel_parser import ExcelTableParser
from utils.marks.analyze import analyze_schemas
from utils.marks.mailer import MarkMailer


async def update_marks(bot: Bot, mail: bool = True):
    data_io: BytesIO = await GoogleExcelDownloader.download(
        doc_id=settings.TABLE_ID
    )
    new_study_mark_schemas, practice_mark_schemas = await ExcelTableParser.parse_file(data_io)
    old_study_mark_schemas: list[SStudyMarkOut] = await StudyMark.gel_all()

    analyze = analyze_schemas(
        new_schemas=new_study_mark_schemas,
        old_schemas=old_study_mark_schemas
    )
    updated_schemas = analyze.updated_schemas
    added_schemas = analyze.added_schemas
    unused_schemas = analyze.unused_schemas

    await StudyMark.clear_id_list(
        [update.old_schema.id for update in updated_schemas] + [schema.id for schema in unused_schemas]
    )
    await StudyMark.set_data([update.new_schema for update in updated_schemas] + added_schemas)

    if mail:
        await MarkMailer(bot=bot).mail_study(analyze=analyze)

    await PracticeMark.set_data(practice_mark_schemas)
