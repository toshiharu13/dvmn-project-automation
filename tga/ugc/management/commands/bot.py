import datetime

from environs import Env
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
)
from telegram.utils.request import Request
from collections import defaultdict


from ugc.models import (
    StudentLevels,
    Students,
    ProjectManagers,
    PMWorkTime,
)


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f"Произошла ошибка: {e}"
            print(error_message)
            raise e

    return inner


@log_errors
def start(update, context):
    ...


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
            states={},
            fallbacks=[CommandHandler("end", end)],
        )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()


prod_mabagers = ProjectManagers.objects.all()
juniors_students = Students.objects.filter(student_level__level_name='Джун')
novice_plus_students = Students.objects.filter(
    student_level__level_name='Новичек+')
novice_students = Students.objects.filter(student_level__level_name='Новичек')
pms_worktime = defaultdict(list)
time_blocks = defaultdict(str)
for prod_manager in prod_mabagers:
    working_time = PMWorkTime.objects.filter(project_manager__pk=prod_manager.pk)
    for working_time_block in working_time:
        pms_worktime[f'{working_time_block.works_from}_{working_time_block.works_to}'] = [working_time_block.works_from, working_time_block.works_to]
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
        time_blocks[f'{(converted_from - delta).time()}-{(converted_from).time()}'] = [(converted_from - delta), (converted_from)]


print(time_blocks)

# временный принты
#print(pms_worktime)
#print(f'Джуны: {juniors_students}')
#print(f'Новички плюс: {novice_plus_students}')
#print(f'Новички: {novice_students}')
