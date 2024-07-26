import logging
from prompts.constances.colors import COLORS
from prompts.constances.styles import STYLES
from prompts.models import Style, Color
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


def create_color():
    Color.objects.bulk_create([Color(color=color) for short_cut, color in COLORS.items()])
    return len(COLORS)

def create_styles():
    Style.objects.bulk_create([Style(style=style) for short_cut, style in STYLES.items()])
    return len(STYLES)


def create_color():
    for short_cut, color in COLORS.items():
        try:
            if Color.objects.all().count() == 0:
                new_obj = Color.objects.create(color=color)
                logging.info(f"Created color object: {new_obj}")
        except Exception as e:
            logging.error(f"Error creating color object: {e}")

def create_styles():
    for short_cut, style in STYLES.items():
        try:
            if Style.objects.all().count() == 0:
                new_obj = Style.objects.create(style=style)
                logging.info(f"Created style object: {new_obj}")
        except Exception as e:
            logging.error(f"Error creating style object: {e}")


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    def handle(self, *args, **options):
        self.stdout.write('filling database...')
        create_color()
        create_styles()