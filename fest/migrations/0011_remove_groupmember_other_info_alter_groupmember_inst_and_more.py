# Generated by Django 4.2 on 2024-02-27 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0010_alter_groupmember_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmember',
            name='other_info',
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='inst',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]