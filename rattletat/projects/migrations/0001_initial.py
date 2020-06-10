# Generated by Django 3.0.6 on 2020-06-04 12:09

from django.db import migrations, models
import rattletat.projects.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('technology', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=rattletat.projects.models.Project._image_path)),
            ],
        ),
    ]
