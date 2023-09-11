from django import forms

class NoTideAccountForm(forms.Form):
    project_choices = [
        ('maac2-hawaii', 'MAAC2 - Hawaii'), 
        ('maac2-idaho', 'MAAC2 - Idaho'), 
        ('maac2-washington', 'MAAC2 - Washington'), 
        ('ohio', 'Ohio'),
        ('texas', 'Texas'),
        ]

    project = forms.ChoiceField(choices=project_choices, required=True)

class EmailTemplateForm(forms.Form):
    greeting_choices = [
        ('Hello', 'Hello'),
        ('Greetings', 'Greetings'),
        ('Good Morning', 'Good Morning'),
        ('Good Afternoon', 'Good Afternoon'),
        ('Good Evening', 'Good Evening'),
    ]

    closing_choices = [
        ('Thank you', 'Thank you'),
        ('Best Regards', 'Best Regards'),
        ('Regards', 'Regards'),
    ]

    greeting = forms.ChoiceField(choices=greeting_choices, required=True, label="Greeting")
    closing = forms.ChoiceField(choices=closing_choices, required=True, label="Closing")
    user_name = forms.CharField(max_length=100, required=True, label="User's Full Name")
    case_number = forms.IntegerField(required=True, label="Case Number")
    agent_name = forms.CharField(max_length=1200, required=True, label="Agent's Name (first name and last initial)")

class TexasEmailTemplateForm(EmailTemplateForm):
    coordinator_choices = [
        ('District Testing Coordinator', 'District Testing Coordinator'),
        ('Campus Testing Coordinator', 'Campus Testing Coordinator'),
    ]

    testing_coordinator = forms.ChoiceField(choices=coordinator_choices, required=True, label="Testing Coordinator")
    coordinator_name = forms.CharField(max_length=100, required=True, label="Coordinator's Name")
    coordinator_email = forms.EmailField(required=True, label="Coordinator's Email")

class OhioEmailtemplateForm(EmailTemplateForm):
    coordinator_choices = [
        ('Building Testing Coordinator', 'Building Testing Coordinator'),
        ('District Administrator', 'District Administrator'),
        ('District Testing Coordinator', 'District Testing Coordinator'),
    ]

    testing_coordinator = forms.ChoiceField(choices=coordinator_choices, required=True, label="Testing Coordinator Type")
    coordinator_name_one = forms.CharField(max_length=100, required=True, label="Coordinator's Name 1")
    coordinator_email_one = forms.EmailField(required=True, label="Coordinator's Email 1")
    coordinator_name_two = forms.CharField(max_length=100, required=False, label="Coordinator's Name 2")
    coordinator_email_two = forms.EmailField(required=False, label="Coordinator's Email 2")
    coordinator_name_three = forms.CharField(max_length=100, required=False, label="Coordinator's Name 3")
    coordinator_email_three = forms.EmailField(required=False, label="Coordinator's Email 3")

class MAAC2WashingtonTemplateForm(EmailTemplateForm):
    coordinator_choices = [
        ('School Coordinator', 'School Coordinator'),
        ('District Coordinator', 'District Coordinator'),
    ]

    testing_coordinator = forms.ChoiceField(choices=coordinator_choices, required=True, label="Testing Coordinator Type")
    coordinator_name_one = forms.CharField(max_length=100, required=True, label="Coordinator's Name 1")
    coordinator_email_one = forms.EmailField(required=True, label="Coordinator's Email 1")
    coordinator_name_two = forms.CharField(max_length=100, required=False, label="School Coordinator's Name 2")
    coordinator_email_two = forms.EmailField(required=False, label="Coordinator's Email 2")
    coordinator_name_three = forms.CharField(max_length=100, required=False, label="School Coordinator's Name 3")
    coordinator_email_three = forms.EmailField(required=False, label="Coordinator's Email 3")

class MAAC2IdahoTemplateForm(EmailTemplateForm):
    coordinator_choices = [
        ('School Coordinator', 'School Coordinator'),
        ('District Coordinator', 'District Coordinator'),
    ]

    testing_coordinator = forms.ChoiceField(choices=coordinator_choices, required=True, label="Testing Coordinator Type")
    coordinator_name_one = forms.CharField(max_length=100, required=True, label="Coordinator's Name 1")
    coordinator_email_one = forms.EmailField(required=True, label="Coordinator's Email 1")
    coordinator_name_two = forms.CharField(max_length=100, required=False, label="School Coordinator's Name 2")
    coordinator_email_two = forms.EmailField(required=False, label="Coordinator's Email 2")
    coordinator_name_three = forms.CharField(max_length=100, required=False, label="School Coordinator's Name 3")
    coordinator_email_three = forms.EmailField(required=False, label="Coordinator's Email 3")

class MAAC2HawaiiTemplateForm(EmailTemplateForm):
    coordinator_choices = [
        ('Principal', 'Principal'),
        ('Test Coordinator', 'Test Coordinator'),
    ]

    testing_coordinator = forms.ChoiceField(choices=coordinator_choices, required=True, label="Testing Coordinator Type")
    coordinator_name_one = forms.CharField(max_length=100, required=True, label="Coordinator's Name 1")
    coordinator_email_one = forms.EmailField(required=True, label="Coordinator's Email 1")
    coordinator_name_two = forms.CharField(max_length=100, required=False, label="School Coordinator's Name 2")
    coordinator_email_two = forms.EmailField(required=False, label="Coordinator's Email 2")
    coordinator_name_three = forms.CharField(max_length=100, required=False, label="School Coordinator's Name 3")
    coordinator_email_three = forms.EmailField(required=False, label="Coordinator's Email 3")