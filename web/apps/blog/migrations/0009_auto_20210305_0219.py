# Generated by Django 3.1.7 on 2021-03-05 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210305_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomponent',
            name='javascript',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postcomponent',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]