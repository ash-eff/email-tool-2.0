# Generated by Django 4.2.5 on 2023-09-13 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_tool', '0016_customformfield_greeting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customformfield',
            name='choices',
            field=models.CharField(blank=True, choices=[('ChoiceField', 'ChoiceField'), ('IntegerField', 'IntegerField'), ('CharField', 'CharField'), ('EmailField', 'EmailField')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customformfield',
            name='label',
            field=models.CharField(choices=[('greeting', 'Greeting'), ('closing', 'Closing'), ('user_name', 'User Name'), ('user_email', 'User Email'), ('case_number', 'Case Number'), ('agent_name', 'Agent Name'), ('coordinator_choices', 'Coordinator Choices'), ('coordinator_name', 'Coordinator Name'), ('coordinator_email', 'Coordinator Email'), ('coordinator_phone', 'Coordinator Phone')], max_length=20),
        ),
        migrations.AlterField(
            model_name='customformfield',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='email_tool.project'),
            preserve_default=False,
        ),
    ]
