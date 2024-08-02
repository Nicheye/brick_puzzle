# Generated by Django 5.0 on 2024-08-02 19:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('BW', 'Black and white'), ('Yel', 'Yellow'), ('br', 'Bright'), ('dr', 'Dark and gloomy'), ('pl', 'Pastel colors')], default='Pastel colors', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(choices=[('AN', 'Anime'), ('GOTH', 'Gothic'), ('Sci-Fi', 'Science and Fiction'), ('CNM', 'Cinematic'), ('MN', 'Minimalistic')], default='Gothic', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=500)),
                ('position', models.IntegerField(null=True)),
                ('image', models.ImageField(upload_to='media/images')),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prompts.color')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prompts.style')),
            ],
        ),
    ]
