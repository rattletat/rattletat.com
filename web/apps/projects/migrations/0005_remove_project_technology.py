# Generated by Django 3.0.6 on 2020-07-15 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20200713_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='technology',
        ),
    ]