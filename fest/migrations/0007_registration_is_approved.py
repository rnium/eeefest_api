# Generated by Django 4.2 on 2024-02-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0006_groupmember_other_info_alter_groupmember_dept_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
