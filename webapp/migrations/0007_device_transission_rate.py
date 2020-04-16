# Generated by Django 2.1.14 on 2020-04-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_gatewaylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='transission_rate',
            field=models.IntegerField(choices=[(6, '6 minutes'), (12, '12 minutes'), (30, '30 minutes'), (60, '60 minutes')], default=6),
            preserve_default=False,
        ),
    ]