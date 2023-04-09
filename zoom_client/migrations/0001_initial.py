# Generated by Django 3.2.18 on 2023-04-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreMetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_code', models.CharField(max_length=50)),
                ('meeting_password', models.CharField(max_length=50)),
                ('participant', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]