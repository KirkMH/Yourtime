# Generated by Django 4.0 on 2024-04-05 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_mob_num_alter_client_tel_num'),
        ('joborder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joborder',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='client_jo', to='client.client', verbose_name='Client'),
            preserve_default=False,
        ),
    ]
