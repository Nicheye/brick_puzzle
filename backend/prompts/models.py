from django.db import models
from authentification.models import User
from prompts.constances.styles import STYLES
from prompts.constances.colors import COLORS

class Style(models.Model):
    style = models.CharField(max_length=30, choices=STYLES, default='Gothic')


class Color(models.Model):
    color = models.CharField(max_length=20, choices=COLORS, default='Pastel colors')


class Prompt(models.Model):
    prompt = models.CharField(max_length=500)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    position = models.IntegerField(null=True)
    image = models.ImageField(upload_to=f'backend/media/images')
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)