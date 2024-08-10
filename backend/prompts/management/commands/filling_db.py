
from prompts.constances.colors import COLORS
from prompts.constances.styles import STYLES
from prompts.models import Style, Color
from django.core.management import BaseCommand


def create_color():
    Color.objects.bulk_create([Color(color=short_cut) for short_cut, color in COLORS.items()])
    return len(COLORS)


def create_styles():
    Style.objects.bulk_create([Style(style=short_cut) for short_cut, style in STYLES.items()])
    return len(STYLES)


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    def handle(self, *args, **options):
        self.stdout.write('filling database...')
        create_color()
        create_styles()
