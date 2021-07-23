# Generated by Django 3.2.1 on 2021-07-23 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0001_initial'),
        ('funds', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fund',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentmodel'),
        ),
        migrations.AddField(
            model_name='fund',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.wallet'),
        ),
    ]
