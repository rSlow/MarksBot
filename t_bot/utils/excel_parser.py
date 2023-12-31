import datetime as dt
import re
from functools import partial
from io import BytesIO

import pandas as pd
from loky import ProcessPoolExecutor

from ORM.schemas import SStudyMarkIn, SPracticeMarkIn
from config import settings
from config.logger import logger
from utils.decorators import TimeCounter, set_async


class ExcelTableParser:
    MAIN_BLOCK_ROW_END = 196

    @staticmethod
    def _get_clean_group(group: str):
        f, n = group.split("-")
        return n + f

    @classmethod
    def _parse_practice_marks(cls,
                              data: BytesIO):
        logger.info(f"Parsing practice marks")
        excel: pd.DataFrame = pd.read_excel(
            data,
            sheet_name="Для НА",
            header=None,
        )
        practice_header_indexes: list[int] = excel[excel[2].str.contains("по практике", na=False)].index.tolist()

        practice_marks: list[SPracticeMarkIn] = []

        if len(practice_header_indexes) == 1:
            practice_header_index = practice_header_indexes[0]
            fio_rows: pd.DataFrame = excel.iloc[practice_header_index + 2:, :]
            for index, fio_row in fio_rows.iterrows():
                fio = fio_row[3]
                group = fio_row[4]
                clean_group = cls._get_clean_group(group)
                course = int(clean_group[0])
                dates_str: list[str] = re.findall(r"\d{2}.\d{2}.\d{4}", fio_row[5])
                for date_str in dates_str:
                    date_obj = dt.datetime.strptime(date_str, "%d.%m.%Y").date()
                    practice_marks.append(SPracticeMarkIn(
                        fio=fio,
                        date=date_obj,
                        group=clean_group,
                        course=course,
                    ))
        else:
            logger.error("Error with get start row (header practice table) - len of list of indexes not equal 1")

        return practice_marks

    @classmethod
    def _parse_group_sheet(cls,
                           data: BytesIO,
                           group: str):
        logger.info(f"Parsing table {group}")

        course = int(group[0])

        data.seek(0)
        excel: pd.DataFrame = pd.read_excel(
            data,
            sheet_name=group,
            header=None,
        )

        _, rows_count = excel.shape
        group_sql_marks: list[SStudyMarkIn] = []

        # отрезаем кусок с импортом двоек за предыдущий месяц
        main_fio_ser: pd.Series = excel[3][:cls.MAIN_BLOCK_ROW_END]
        # индексы ячеек с <ФИО>, для отсчета недель
        week_limiter_indexes: list[int] = main_fio_ser[main_fio_ser == "ФИО"].index.to_list() + [cls.MAIN_BLOCK_ROW_END]

        for week_num, start_week_idx in enumerate(week_limiter_indexes[:-1]):  # индекс стартовой строки недели
            end_week_idx = week_limiter_indexes[week_num + 1] - 1  # индекс последней строки недели
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
                        logger.warning("ERROR WITH PARSE PAIR NUMBER")
                        pair_num = 0
                    subject_name = week_header_df.iloc[2, pair_start_index]  # название предмета

                    pair_mark_index_first = pair_start_index  # первая колонка оценок пары
                    pair_mark_index_second = pair_start_index + 1  # вторая колонка оценок пары

                    for pair_mark_index in [pair_mark_index_first, pair_mark_index_second]:
                        pair_marks_ser: pd.Series = fio_week_df.iloc[:, pair_mark_index]  # колонка оценок
                        # проверка соответствия индексов
                        if pair_marks_ser.index.tolist() != fio_week_col.index.tolist():
                            message = (f"Error within parsing file: indexes 'pair_marks_ser' not equal to indexes "
                                       f"<fio_week_col>: {pair_marks_ser.index.tolist() = }, "
                                       f"{fio_week_col.index.tolist() = }, {date = }, "
                                       f"{subject_name = }, {pair_mark_index = }")
                            logger.exception(message)
                            raise RuntimeError(message)

                        for index, mark in pair_marks_ser[pair_marks_ser.notnull()].items():
                            fio = fio_week_col[index].strip()  # получение ФИО
                            string_mark = str(int(mark)) if isinstance(mark, (int, float)) else mark
                            group_sql_marks.append(SStudyMarkIn(
                                fio=fio,
                                date=date,
                                subject=subject_name,
                                pair_number=pair_num,
                                mark=string_mark,
                                group=group,
                                course=course,
                                mark_num_index=(pair_mark_index != pair_mark_index_first) + 1
                            ))

            # парсинг оценок за прошлый месяц
            if week_num == 0:  # только первая итерация
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
                    prev_mark_strings: list[str] = value.split()  # разделение на список оценок
                    for prev_mark_string in prev_mark_strings:
                        prev_mark_string = prev_mark_string.replace(")", "")
                        # деление на предмет и дату
                        prev_subject_name, prev_string_date, *_ = prev_mark_string.split("(")
                        now = dt.date.today()
                        # подготовка даты
                        prev_date = dt.datetime.strptime(
                            f"{prev_string_date}.{now.year}",
                            "%d.%m.%Y"
                        ).date()
                        group_sql_marks.append(SStudyMarkIn(
                            fio=fio,
                            date=prev_date,
                            subject=prev_subject_name,
                            mark="2",
                            group=group,
                            course=course,
                            mark_num_index=1,
                            is_in_last_month=True
                        ))

        return group_sql_marks

    @classmethod
    @TimeCounter.a_sync
    @set_async
    def parse_file(cls, data: BytesIO):
        logger.info("Start parsing table")

        sheet_names = settings.GROUPS
        with ProcessPoolExecutor(len(sheet_names)) as pool:
            mark_sheets_schemas: list[list[SStudyMarkIn]] = [*pool.map(
                partial(cls._parse_group_sheet, data),
                sheet_names
            )]
        study_mark_schemas: list[SStudyMarkIn] = []
        for mark_sheet_schemas in mark_sheets_schemas:
            study_mark_schemas.extend(mark_sheet_schemas)

        practice_mark_schemas = cls._parse_practice_marks(data=data)
        return study_mark_schemas, practice_mark_schemas
