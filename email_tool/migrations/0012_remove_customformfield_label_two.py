# Generated by Django 4.2.5 on 2023-09-22 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0011_alter_customformfield_label_two'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customformfield',
            name='label_two',
        ),
    ]
