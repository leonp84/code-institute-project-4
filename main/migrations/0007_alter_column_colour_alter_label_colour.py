# Generated by Django 5.0.6 on 2024-05-10 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_task_label_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='colour',
            field=models.CharField(default='white'),
        ),
        migrations.AlterField(
            model_name='label',
            name='colour',
            field=models.CharField(default='white'),
        ),
    ]
