# Generated by Django 5.0.6 on 2024-05-13 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_board_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
