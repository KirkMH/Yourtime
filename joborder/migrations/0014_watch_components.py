# Generated by Django 4.0 on 2024-04-16 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joborder', '0013_remove_watch_aesthetic_defects_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='components',
            field=models.CharField(default='', max_length=100, verbose_name='Components'),
            preserve_default=False,
        ),
    ]
