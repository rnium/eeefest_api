# Generated by Django 4.2 on 2024-02-18 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest', models.CharField(choices=[('lfr', 'Line Following'), ('poster', 'Poster Presentation'), ('circuit-solve', 'Circuit Solve'), ('integration', 'Integration'), ('gaming-fifa', 'Gaming [FIFA]'), ('gaming-chess', 'Gaming [Chess]')], max_length=20)),
                ('name', models.CharField(max_length=500)),
                ('team_name', models.CharField(max_length=500, null=True)),
                ('email', models.EmailField(max_length=500)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('transaction_id', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
    ]
