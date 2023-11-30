from datetime import date, timedelta

from aiogram import Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession

from FSM.start import CommonState
from ORM.marks.practice import PracticeMark
from ORM.marks.study import StudyMark
from jinja import render_template
from keyboards.start import StartKeyboard

common_marks_router = Router(name="common_marks")


@common_marks_router.message(
    CommonState.start,
    F.text == StartKeyboard.Buttons.two_faculty
)
async def two_faculty(message: types.Message, session: AsyncSession):
    twos_marks = await StudyMark.get_two_faculty_info(session)
    averages = await StudyMark.get_faculty_average(session)

    info = {}
    for two_mark in twos_marks:
        course, twos, marks = two_mark
        info.setdefault(course, {})
        info[course]["twos"] = twos
        info[course]["marks"] = marks
    for average in averages:
        course, avg = average
        info[course]["avg"] = avg

    text = render_template(
        template_name="two_faculty.jinja2",
        data={"info": info}
    )
    await message.answer(text)


@common_marks_router.message(
    CommonState.start,
    F.text == StartKeyboard.Buttons.two_today
)
async def two_today(message: types.Message, session: AsyncSession):
    today_marks = await StudyMark.get_two_today_info(session)
    text = render_template(
        template_name="two_faculty_today.jinja2",
        data={"marks": today_marks}
    )
    await message.answer(text)


@common_marks_router.message(
    CommonState.start,
    F.text == StartKeyboard.Buttons.two_long_two_weeks
)
async def two_long_two_weeks(message: types.Message, session: AsyncSession):
    twos_long_two_weeks = await StudyMark.get_twos_long_two_weeks(session)
    fios = {}
    for mark in twos_long_two_weeks:
        fio_marks = fios.get(mark.fio, [])
        fio_marks.append(mark)
        fios[mark.fio] = fio_marks

    text = render_template(
        template_name="two_faculty_long_two_weeks.jinja2",
        data={
            "fios": fios,
            "two_weeks_ago": date.today() - timedelta(weeks=2)
        }
    )
    await message.answer(text)


@common_marks_router.message(
    CommonState.start,
    F.text == StartKeyboard.Buttons.two_practice
)
async def two_practice(message: types.Message, session: AsyncSession):
    mark_schemas: list[PracticeMark] = await PracticeMark.get_all(session)
    fio_count, mark_count = await PracticeMark.get_info(session)
    text = render_template(
        template_name="two_practice.jinja2",
        data={
            "mark_schemas": mark_schemas,
            "fio_count": fio_count,
            "mark_count": mark_count
        }
    )
    await message.answer(text)
