# Generated by Django 2.1.14 on 2020-01-14 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20200114_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='transmissions',
        ),
        migrations.AddField(
            model_name='transmission',
            name='device',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webapp.Device'),
            preserve_default=False,
        ),
    ]