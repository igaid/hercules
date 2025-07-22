from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Χρήστης', max_length=50)
    password = forms.CharField(label='Κωδικός πρόσβασης', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Λανθασμένα στοιχεία εισόδου. Παρακαλώ προσπαθήστε ξανά.'
        super().__init__(*args, **kwargs)
