# Generated by Django 2.1.14 on 2020-01-21 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200114_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='transmission',
            name='voltage',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]