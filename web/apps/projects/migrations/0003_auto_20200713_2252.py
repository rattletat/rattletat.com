# Generated by Django 3.0.6 on 2020-07-13 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200713_2226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['position']},
        ),
        migrations.RemoveField(
            model_name='component',
            name='order',
        ),
        migrations.AddField(
            model_name='component',
            name='position',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]