# Generated by Django 5.1.3 on 2024-12-25 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_paymentinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentInfo',
        ),
    ]
