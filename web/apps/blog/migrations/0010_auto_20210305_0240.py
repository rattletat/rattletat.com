# Generated by Django 3.1.7 on 2021-03-05 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210305_0219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomponent',
            name='javascript',
        ),
        migrations.AddField(
            model_name='post',
            name='javascript',
            field=models.TextField(blank=True, null=True),
        ),
    ]
