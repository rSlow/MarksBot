from io import BytesIO
import asyncio

from ORM.marks import Mark
from ORM.schemas import SMarkIn
from config import settings
from utils.decors import time_count
from utils.downloader import GoogleExcelDownloader
from utils.excel_parser import ExcelTableParser


async def update_marks():
    data_io: BytesIO = await GoogleExcelDownloader.download(
        doc_id=settings.TABLE_ID
    )
    sql_marks: list[SMarkIn] = ExcelTableParser.parse_file(data_io)
    await Mark.set_data(sql_marks)


if __name__ == '__main__':
    @time_count
    def main():
        asyncio.run(update_marks())


    main()
