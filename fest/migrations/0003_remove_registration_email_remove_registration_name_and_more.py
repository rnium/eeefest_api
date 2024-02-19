# Generated by Django 4.2 on 2024-02-19 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0002_registration_gateway'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='email',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='name',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='phoneNumber',
        ),
        migrations.AddField(
            model_name='registration',
            name='group_members_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='registration',
            name='paying_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='team_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('inst', models.CharField(max_length=200)),
                ('dept', models.CharField(max_length=100)),
                ('tshirt_size', models.CharField(max_length=5)),
                ('phone', models.CharField(max_length=5)),
                ('email', models.EmailField(max_length=254)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fest.registration')),
            ],
        ),
    ]
