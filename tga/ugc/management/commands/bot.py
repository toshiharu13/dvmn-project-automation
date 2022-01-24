import datetime
import random
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from environs import Env
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)
from telegram.utils.request import Request
from ugc.models import (PMWorkTime, ProjectManagers, Projects, StudentLevels,
                        Students, StudentsWorkTime)

FILL_BASE = range(1)


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f"Произошла ошибка: {e}"
            print(error_message)
            raise e
    return inner


def fill_student_call_table(time_blocks, student):
    time_block = random.choice(list(time_blocks))
    StudentsWorkTime.objects.update_or_create(
        project=Projects.objects.all().first(),
        student=get_object_or_404(Students, pk=student.pk),
        defaults={'works_from': time_blocks[time_block][0],
                  'works_to': time_blocks[time_block][1]},
    )[0]

def randomly_fill_students_call(time_blocks):
    juniors_students = Students.objects.filter(student_level__level_name='Джун')
    novice_plus_students = Students.objects.filter(
        student_level__level_name='Новичек+')
    novice_students = Students.objects.filter(
        student_level__level_name='Новичек')
    for jun_student in juniors_students:
        fill_student_call_table(time_blocks, jun_student)
    for nov_plus_student in novice_plus_students:
        fill_student_call_table(time_blocks, nov_plus_student)
    for nov_student in novice_students:
        fill_student_call_table(time_blocks, nov_student)
    print(StudentsWorkTime.objects.all())



@log_errors
def start(update, context):
    prod_mabagers = ProjectManagers.objects.all()
    pms_worktime = defaultdict(list)
    global time_blocks
    for prod_manager in prod_mabagers:
        working_time = PMWorkTime.objects.filter(
            project_manager__pk=prod_manager.pk)
        for working_time_block in working_time:
            pms_worktime[
                f'{working_time_block.works_from}_{working_time_block.works_to}'] = [
                working_time_block.works_from, working_time_block.works_to]
    for from_to_timepoint in pms_worktime:
        delta = datetime.timedelta(minutes=30)
        hour_from = pms_worktime[from_to_timepoint][0]
        hour_to = pms_worktime[from_to_timepoint][1]
        converted_from = datetime.datetime.strptime(
            f'{hour_from.hour}:{hour_from.minute}', '%H:%M')
        convert_to = datetime.datetime.strptime(
            f'{hour_to.hour}:{hour_to.minute}', '%H:%M')
        while converted_from <= convert_to + delta:
            converted_from += delta
            time_blocks[
                f'{(converted_from - delta).time()}-{(converted_from).time()}'] = [(converted_from - delta), (converted_from)]

    keyboard = []
    for key in list(time_blocks.keys()):
        keyboard.append(
            [InlineKeyboardButton(text=key, callback_data=str(key))]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Выбирите удобное время созвона",
        reply_markup=reply_markup,
    )
    # в случае необходимости, рандомно заполнить таблицу созвонов студентов
    #randomly_fill_students_call(time_blocks)
    return FILL_BASE


@log_errors
def fill_students_worktime_table(update, context):
    user_id = update['_effective_user']['id']
    time_blocks_from_to = update['callback_query']['data']
    student = get_object_or_404(Students, telegram_id=user_id)

    StudentsWorkTime.objects.update_or_create(
        project=Projects.objects.all().first(),
        student=get_object_or_404(Students, pk=student.pk),
        defaults={'works_from': time_blocks[time_blocks_from_to][0],
                  'works_to': time_blocks[time_blocks_from_to][1]},
    )[0]


@log_errors
def end(update, context):
    ...


class Command(BaseCommand):
    help = "Телеграм-бот"

    def handle(self, *args, **options):
        env = Env()
        env.read_env()
        TG_TOKEN = env.str("TG_TOKEN")

        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=TG_TOKEN,
            base_url=getattr(settings, "PROXY_URL", None),
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                FILL_BASE: [
                    CallbackQueryHandler(fill_students_worktime_table, pattern='\S')
                ],
            },
            fallbacks=[CommandHandler("end", end)],
        )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()


time_blocks = defaultdict(str)

