# Generated by Django 4.0 on 2024-10-15 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_mob_num_alter_client_tel_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['name']},
        ),
    ]
