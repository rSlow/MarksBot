import datetime as dt
import re
from io import BytesIO

import pandas as pd

from ORM.schemas import SMarkIn
from config import settings
from config.logger import logger
from utils.decors import time_count


class ExcelTableParser:
    MAIN_BLOCK_ROW_END = 196

    @classmethod
    def _parse_sheet(cls, data: BytesIO, sheet_name: str):
        group = sheet_name
        course = int(group[0])

        data.seek(0)
        excel: pd.DataFrame = pd.read_excel(
            data,
            sheet_name=sheet_name,
            header=None,
        )
        logger.info(f"Parsing table {sheet_name}")

        _, rows_count = excel.shape
        group_sql_marks: list[SMarkIn] = []

        # отрезаем кусок с импортом двоек за предыдущий месяц
        main_fio_ser: pd.Series = excel[3][:cls.MAIN_BLOCK_ROW_END]
        # индексы ячеек с <ФИО>, для отсчета недель
        week_limiter_indexes: list[int] = main_fio_ser[main_fio_ser == "ФИО"].index.to_list() + [cls.MAIN_BLOCK_ROW_END]

        for i, start_week_idx in enumerate(week_limiter_indexes[:-1]):  # индекс стартовой строки недели
            end_week_idx = week_limiter_indexes[i + 1] - 1  # индекс последней строки недели
            week_df: pd.DataFrame = excel.iloc[start_week_idx:end_week_idx]  # получение df недели
            fio_week_df: pd.DataFrame = week_df[
                week_df[3].str.contains(r"\w+ \w\. ?\w\.", flags=re.IGNORECASE, regex=True, na=False)
            ]  # получение df со строками оценок
            fio_week_col: pd.Series = fio_week_df[3]  # колонка с ФИО и индексом строк, для индексов df дней
            week_header_df: pd.DataFrame = week_df.iloc[0:3]  # шапка недели
            # номера столбцов, с которых начинаются дни
            start_day_indexes: list[int] = week_header_df.loc[:, week_header_df.iloc[0] == "Дата:"].columns.to_list()

            for start_day_index in start_day_indexes:
                date = dt.date(
                    day=week_header_df.iloc[0, start_day_index + 2],
                    month=week_header_df.iloc[0, start_day_index + 4],
                    year=week_header_df.iloc[0, start_day_index + 6]
                )  # дата дня

                for pair_start_index in range(start_day_index, start_day_index + 8, 2):
                    try:  # номер пары
                        pair_num = int(week_header_df.iloc[1, pair_start_index][0])
                    except ValueError:
                        logger.warning("ERROR WITH PARSE PAIR NUMBER")  # CHANGE TO LOGGING
                        pair_num = 0
                    subject_name = week_header_df.iloc[2, pair_start_index]  # название предмета

                    pair_mark_index_first = pair_start_index  # первая колонка оценок пары
                    pair_mark_index_second = pair_start_index + 1  # вторая колонка оценок пары

                    for pair_mark_index in [pair_mark_index_first, pair_mark_index_second]:
                        pair_marks_ser: pd.Series = fio_week_df.iloc[:, pair_mark_index]  # колонка оценок
                        # проверка соответствия индексов
                        if pair_marks_ser.index.tolist() != fio_week_col.index.tolist():
                            message = (f"Error within parsing file: indexes <pair_marks_ser> not equal to indexes "
                                       f"<fio_week_col>: {pair_marks_ser.index.tolist() = }, "
                                       f"{fio_week_col.index.tolist() = }, {date = }, "
                                       f"{subject_name = }, {pair_mark_index = }")
                            logger.exception(message)
                            raise RuntimeError(message)

                        for index, mark in pair_marks_ser[pair_marks_ser.notnull()].items():
                            fio = fio_week_col[index].strip()  # получение ФИО
                            string_mark = str(int(mark)) if isinstance(mark, (int, float)) else mark
                            group_sql_marks.append(SMarkIn(
                                fio=fio,
                                date=date,
                                subject=subject_name,
                                pair_number=pair_num,
                                mark=string_mark,
                                group=group,
                                course=course
                            ))

            # парсинг оценок за прошлый месяц
            if i == 0:  # только первая итерация
                start_prev_month_block = cls.MAIN_BLOCK_ROW_END + 2  # начало и конец блока -VVV-
                end_prev_month_block = start_prev_month_block + (week_limiter_indexes[1] - week_limiter_indexes[0])
                prev_month_block: pd.DataFrame = excel.iloc[start_prev_month_block:end_prev_month_block]  # df блока
                marks_col: pd.Series = prev_month_block.iloc[:, 5]  # колонка с оценками
                first_fio_index = fio_week_col.index.tolist()[0]  # начальный индекс с ФИО
                marks_col.index = pd.RangeIndex(
                    start=first_fio_index,
                    stop=first_fio_index + len(marks_col),
                    step=1
                )  # переиндексация под индексы ФИО, для сопоставления

                for prev_index, value in marks_col[marks_col.notnull()].items():
                    fio = fio_week_col[prev_index]  # получение ФИО
                    prev_mark_strings: list[str] = value.split()
                    for prev_mark_string in prev_mark_strings:
                        prev_mark_string = prev_mark_string.replace(")", "")
                        prev_subject_name, prev_string_date, *_ = prev_mark_string.split("(")
                        now = dt.date.today()
                        prev_date = dt.datetime.strptime(
                            f"{prev_string_date}.{now.year}",
                            "%d.%m.%Y"
                        ).date()
                        group_sql_marks.append(SMarkIn(
                            fio=fio,
                            date=prev_date,
                            subject=prev_subject_name,
                            mark="2",
                            group=group,
                            course=course
                        ))

        return group_sql_marks

    @classmethod
    @time_count
    def parse_file(cls, data: BytesIO):
        logger.info("Start parsing table")

        sql_marks: list[SMarkIn] = []
        sheet_names = settings.GROUPS
        for sheet_name in sheet_names:
            sql_marks.extend(cls._parse_sheet(
                data=data,
                sheet_name=sheet_name
            ))
        return sql_marks
