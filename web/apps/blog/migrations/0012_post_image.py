# Generated by Django 3.1.7 on 2022-10-21 22:13

import apps.blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210306_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=apps.blog.models.Post._image_path),
        ),
    ]
