from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Code

User = get_user_model()



class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs= {'autofocus': True, 'placeholder':'Enter Email','class':'form-control'}))
    password = forms.CharField(label="Password", strip = False, widget = forms.PasswordInput(attrs = {'autocomplete': 'current-password', 'class':'form-control', 'placeholder':'Enter Password'}))

class password_user_change(PasswordChangeForm):
    old_password = forms.CharField(widget= forms.PasswordInput(attrs= {'autocomplete': 'current-password', 'autofocus': True, 'placeholder': "Enter Old Password"}))

    new_password1 = forms.CharField(strip= False, widget= forms.PasswordInput(attrs={'autocomplete': 'new_password', 'placeholder': "Enter New Password"}), help_text = password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'new_password', 'placeholder': "Confirm New Password"}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length = 254, widget= forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Email Address'}))



class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, help_text= password_validation.password_validators_help_text_html)
    new_password2 = forms.CharField(label=_('Confirm Password'), strip=False)


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"),strip= False, widget= forms.PasswordInput(attrs={'autocomplete': 'new_password', 'class': 'form-control'}), help_text = password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_('Confirm New Password'), strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'new_password', 'class':'form-control'}))



class CodeForm(forms.ModelForm):
    number = forms.CharField(label = 'Code', help_text='Enter The SMS verification code here')
    class Meta:
        model = Code
        fields = ('number',)