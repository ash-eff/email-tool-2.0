# Generated by Django 4.2.5 on 2023-09-21 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0002_remove_customformfield_projects_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customformfield',
            name='template_code',
            field=models.CharField(default='', max_length=61),
        ),
        migrations.AddField(
            model_name='customformfield',
            name='template_format',
            field=models.CharField(default='', max_length=62),
        ),
    ]
