# Generated by Django 4.2.5 on 2023-09-21 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0004_alter_customformfield_template_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customformtemplate',
            name='template_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customformfield',
            name='label',
            field=models.CharField(choices=[('Greeting', 'Greeting'), ('Closing', 'Closing'), ('User Name', 'User Name'), ('User Email', 'User Email'), ('Case Number', 'Case Number'), ('Agent Name', 'Agent Name'), ('Coordinator Choices', 'Coordinator Choices'), ('Coordinator Choices Abbreviated', 'Coordinator Choices Abbreviated'), ('Coordinator Name', 'Coordinator Name'), ('Coordinator Email', 'Coordinator Email'), ('Coordinator Phone', 'Coordinator Phone'), ('Incorrect EK', 'Incorrect EK'), ('Correct EK', 'Correct EK'), ('School Year', 'School Year'), ('Results ID', 'Results ID'), ('General Choice Field', 'General Choice Field'), ('General Integer Field', 'General Integer Field'), ('General Text Field', 'General Text Field')], max_length=60),
        ),
    ]
