import asyncio
from io import BytesIO

import aiohttp

from config import settings
from config.logger import logger


class GoogleExcelDownloader:
    MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    DOWNLOAD_LINK = ("https://www.googleapis.com/drive/v3/files/{doc_id}/export?"
                     "mimeType={mime_type}&"
                     "key={api_key}")

    @classmethod
    async def download(cls, doc_id: str):
        async with aiohttp.ClientSession() as session:
            logger.info("Start downloading table")
            response = await session.get(cls.DOWNLOAD_LINK.format(
                doc_id=doc_id,
                mime_type=cls.MIME_TYPE,
                api_key=settings.API_KEY
            ))
            data = await response.read()
        data_io = BytesIO(data)
        return data_io


if __name__ == '__main__':
    asyncio.run(GoogleExcelDownloader.download(
        doc_id=settings.TABLE_ID
    ))
