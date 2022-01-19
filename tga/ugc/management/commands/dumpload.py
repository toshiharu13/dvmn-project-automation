import os
from django.core.management.base import BaseCommand, CommandError
from environs import Env

env = Env()
env.read_env()


class Command(BaseCommand):
    help = 'load json data to DB'
    students_json = env.str('STUDENTS_JSON', default='students.json')
    pm_json = env.str('PM_JSON', default='pm.json')

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
            os.system(f'python tga/manage.py loaddata {self.students_json}')
            print('students.json loaded')
        elif options['product_manager']:
            os.system(f'python tga/manage.py loaddata {self.pm_json}')
            print('pm.json loaded')
