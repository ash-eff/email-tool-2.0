# Generated by Django 4.2.5 on 2023-09-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0023_alter_customformfield_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customformtemplate',
            name='project',
        ),
        migrations.AddField(
            model_name='customformtemplate',
            name='template_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='email_templates',
            field=models.ManyToManyField(to='email_tool.customformtemplate'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project',
            field=models.CharField(choices=[('indiana', 'Indiana'), ('maac2-hawaii', 'MAAC2 - Hawaii'), ('maac2-idaho', 'MAAC2 - Idaho'), ('maac2-washington', 'MAAC2 - Washington'), ('ohio', 'Ohio'), ('texas', 'Texas')], max_length=100),
        ),
    ]