from environs import Env
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
)
from telegram.utils.request import Request


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
    pass


@log_errors
def end(update, context):
    pass


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

for prod_manager in prod_mabagers:
    working_time = list(
        PMWorkTime.objects.filter(project_manager__pk=prod_manager.pk))
    print(f'менаджер {prod_manager} время:{working_time}')

#djunes_students =