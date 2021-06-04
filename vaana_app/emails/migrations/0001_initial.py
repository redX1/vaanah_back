# Generated by Django 3.2.1 on 2021-06-01 12:49

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('mail_to', models.EmailField(max_length=50)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField(max_length=2000)),
                ('date_submitted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
