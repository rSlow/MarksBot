import asyncio
from typing import Iterable

from aiogram import Bot

from ORM.mailing import Mailing
from ORM.schemas import SMailing, SMarkIn
from jinja import render_template
from utils.marks.filters import TwoAllFilter, NotTwoAllFilter, TwoMatchAttrFilter, NotTwoMatchAttrFilter
from utils.marks.schemas import SMode, SAnalyze


class MarkMailer:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_one_mail(self,
                            telegram_id: int | str,
                            template_name: str,
                            mark_schemas: Iterable[SMarkIn]):
        text = render_template(
            template_name=template_name,
            data={"mark_schemas": mark_schemas}
        )
        await self.bot.send_message(
            chat_id=telegram_id,
            text=text
        )

    async def send_by_attrs(self,
                            modes: list[SMode],  # режим (поле для фильтра, фильтр)
                            mark_schemas: Iterable[SMarkIn],  # список оценок (измененных, добавленных, удаленных)
                            mailing_schemas: Iterable[SMailing],  # полный список рассылки
                            template_name: str):
        for mode in modes:
            attr = mode.filter_attr
            marks_filter = mode.filter
            attr_tasks = []

            # список уникальных значений подписки по полю (название группы, номер курса и тд)
            sorted_mail_values: set[str] = {getattr(schema, attr) for schema in mailing_schemas if
                                            getattr(schema, attr, None) is not None}
            for sorted_mail_value in sorted_mail_values:
                sorted_mark_schemas: list[SMarkIn] = [*filter(
                    marks_filter(attr, sorted_mail_value),
                    mark_schemas
                )]  # фильтрация оценок по условию <Оценка.Поле.Значение> == <Значение_поля_подписки>
                sorted_mailing_schemas = [
                    mailing_schema for mailing_schema in mailing_schemas
                    if getattr(mailing_schema, attr, None) == sorted_mail_value
                ]  # отбор необходимых учетных записей для рассылки по значению поля подписки

                # проверка существования оценок для отображения и подписчиков
                if sorted_mark_schemas and sorted_mailing_schemas:
                    # перебор подписчиков на конкретное значение подписки
                    for sorted_mailing_schema in sorted_mailing_schemas:
                        attr_tasks.append(self.send_one_mail(
                            telegram_id=sorted_mailing_schema.telegram_id,
                            mark_schemas=sorted_mark_schemas,
                            template_name=template_name
                        ))
            await asyncio.gather(*attr_tasks)  # заменить на stage_gather

    async def mail_all(self, analyze: SAnalyze):
        mailings = await Mailing.get_all()
        mailing_schemas = [SMailing.model_validate(mailing) for mailing in mailings]

        # ОБНОВЛЕННЫЕ (ИСПРАВЛЕНИЯ)
        await self.send_by_attrs(
            modes=[SMode(filter_attr="group", filter=NotTwoMatchAttrFilter),
                   SMode(filter_attr="course", filter=NotTwoMatchAttrFilter),
                   SMode(filter_attr="all", filter=NotTwoAllFilter)],
            mark_schemas=[update.new_schema for update in analyze.updated_schemas],
            mailing_schemas=mailing_schemas,
            template_name="updated_marks.jinja2"
        )
        # НОВЫЕ (ПОЛУЧЕННЫЕ ДВОЙКИ)
        await self.send_by_attrs(
            modes=[SMode(filter_attr="group", filter=TwoMatchAttrFilter),
                   SMode(filter_attr="course", filter=TwoMatchAttrFilter),
                   SMode(filter_attr="all", filter=TwoAllFilter)],
            mark_schemas=analyze.added_schemas,
            mailing_schemas=mailing_schemas,
            template_name="new_marks.jinja2",
        )
