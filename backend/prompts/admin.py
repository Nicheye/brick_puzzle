from django.contrib import admin
from prompts.models import Style, Prompt, Color
# Register your models here.
admin.site.register(Style)
admin.site.register(Prompt)
admin.site.register(Color)
