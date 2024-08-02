# Generated by Django 5.0 on 2024-08-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0004_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
