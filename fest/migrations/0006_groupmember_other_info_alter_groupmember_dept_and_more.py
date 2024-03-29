# Generated by Django 4.2 on 2024-02-19 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0005_rename_tshirt_size_groupmember_tshirt'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='other_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='dept',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='inst',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='phone',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='tshirt',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
