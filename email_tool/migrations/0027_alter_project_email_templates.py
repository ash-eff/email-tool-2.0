# Generated by Django 4.2.5 on 2023-09-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0026_customformtemplate_template_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='email_templates',
            field=models.ManyToManyField(blank=True, null=True, to='email_tool.customformtemplate'),
        ),
    ]
