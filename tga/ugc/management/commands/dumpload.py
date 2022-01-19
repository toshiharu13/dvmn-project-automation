import os
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'load json data to DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--students',
            action='store_true',
            default=False,
            help='Add students data from json',
        )
        parser.add_argument(
            '-p',
            '--product_manager',
            action='store_true',
            default=False,
            help='Add PM data from json',
        )

    def handle(self, *args, **options):
        if options['students']:
            os.system("python tga/manage.py loaddata students.json")
            print('students.json loaded')
        elif options['product_manager']:
            os.system("python tga/manage.py loaddata pm.json")
            print('pm.json loaded')
