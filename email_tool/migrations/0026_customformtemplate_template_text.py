# Generated by Django 4.2.5 on 2023-09-14 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0025_remove_customformtemplate_template_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='customformtemplate',
            name='template_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]