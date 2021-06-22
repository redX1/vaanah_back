# Generated by Django 3.2.1 on 2021-06-21 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shippings', '0001_initial'),
        ('orders', '0002_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shippings.shippingmethod'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('initiated', 'initiated'), ('confirmed', 'confirmed'), ('shipping', 'shipping'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='initiated', max_length=100),
        ),
    ]