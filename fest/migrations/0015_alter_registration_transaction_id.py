# Generated by Django 4.2 on 2024-02-29 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0014_alter_registration_gateway_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
