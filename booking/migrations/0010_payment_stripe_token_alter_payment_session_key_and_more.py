# Generated by Django 4.1 on 2022-09-18 23:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='stripe_token',
            field=models.CharField(max_length=1000, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='session_key',
            field=models.CharField(blank=True, max_length=300, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
