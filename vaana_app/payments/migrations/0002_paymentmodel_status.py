# Generated by Django 3.2.1 on 2021-06-23 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='status',
            field=models.CharField(choices=[('open', 'open'), ('done', 'done')], default='open', max_length=100),
        ),
    ]