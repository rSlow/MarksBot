from io import BytesIO
import asyncio
from pprint import pprint

from ORM.marks import Mark
from ORM.schemas import SMarkIn, SMarkOut
from config import settings
from utils.marks import analyze_schemas
from utils.decors import time_count
from utils.downloader import GoogleExcelDownloader
from utils.excel_parser import ExcelTableParser


async def update_marks():
    data_io: BytesIO = await GoogleExcelDownloader.download(
        doc_id=settings.TABLE_ID
    )
    new_mark_schemas: list[SMarkIn] = ExcelTableParser.parse_file(data_io)
    old_mark_schemas: list[SMarkOut] = await Mark.gel_all()

    updated_schemas, added_schemas, no_more_schemas = analyze_schemas(
        new_schemas=new_mark_schemas,
        old_schemas=old_mark_schemas
    )
    pprint(updated_schemas)
    print("-------")
    pprint(added_schemas)
    print("-------")
    pprint(no_more_schemas)

    await Mark.clear()
    await Mark.set_data(new_mark_schemas)


if __name__ == '__main__':
    @time_count
    def main():
        asyncio.run(update_marks())


    main()
