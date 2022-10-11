# Generated by Django 4.1 on 2022-10-02 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_vehiclereview_placereview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placereview',
            name='percentage',
            field=models.IntegerField(choices=[(20, 20), (40, 40), (60, 60), (80, 80), (100, 100)], null=True),
        ),
        migrations.AlterField(
            model_name='vehiclereview',
            name='percentage',
            field=models.IntegerField(choices=[(20, 20), (40, 40), (60, 60), (80, 80), (100, 100)], null=True),
        ),
    ]