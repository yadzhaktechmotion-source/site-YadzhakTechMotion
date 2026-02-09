from django import forms
from .models import User


class EmailForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'})
    )


class CodeForm(forms.Form):
    code = forms.CharField(
        label="Code",
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456'})
    )


class RegisterForm(forms.ModelForm):
    email_confirm = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your email'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email", "").strip().lower()
        email_confirm = cleaned_data.get("email_confirm", "").strip().lower()
        if email and email_confirm and email != email_confirm:
            raise forms.ValidationError("Emails do not match.")
        return cleaned_data

    def clean_first_name(self):
        first = self.cleaned_data.get('first_name', '').strip()
        if not first:
            raise forms.ValidationError("First name is required.")
        return first

    def clean_last_name(self):
        last = self.cleaned_data.get('last_name', '').strip()
        if not last:
            raise forms.ValidationError("Last name is required.")
        return last
