from django.db import models
from authentification.models import User
from prompts.constances.styles import STYLES
from prompts.constances.colors import COLORS

# Create your models here
class Prompt(models.Model):
    prompt = models.CharField(max_length=500)
    style = models.CharField(max_length=25, choices=STYLES, default='Gothic')
    color = models.CharField(max_length=20, choices=COLORS, default='Pastel colors')
    position = models.IntegerField(null=True)
    image = models.ImageField(upload_to='media/images')
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)