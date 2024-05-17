# Generated by Django 5.0.6 on 2024-05-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_column_colour_alter_column_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='column',
            name='colour',
            field=models.CharField(default='white', max_length=255),
        ),
        migrations.AlterField(
            model_name='column',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='label',
            name='colour',
            field=models.CharField(default='light', max_length=255),
        ),
        migrations.AlterField(
            model_name='label',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
