# Generated by Django 4.2 on 2024-02-19 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0004_groupmember_reg_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupmember',
            old_name='tshirt_size',
            new_name='tshirt',
        ),
    ]
