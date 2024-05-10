# Generated by Django 5.0.6 on 2024-05-10 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_to_board', to='main.board'),
        ),
        migrations.AlterField(
            model_name='label',
            name='colour',
            field=models.CharField(default='light'),
        ),
    ]
