# Generated by Django 4.2.5 on 2023-09-22 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0007_alter_customformfield_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='form_fields_created',
            field=models.BooleanField(default=False),
        ),
    ]
