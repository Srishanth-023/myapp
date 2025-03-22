from django import forms
from django.contrib.auth.models import User

# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(label = "Name", max_length = 100)
    email = forms.EmailField(label = "Email")
    message = forms.CharField(label = "Message")

# Register Form
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label = "Username", max_length = 100, required = True)
    email = forms.EmailField(label = "Email", max_length = 100, required = True)
    password = forms.CharField(label = "Password", max_length = 100, required = True)
    password_confirm = forms.CharField(label = "Confirm Password", max_length = 100, required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']