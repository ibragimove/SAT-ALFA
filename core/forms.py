import re
from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Application
        fields = ['name', 'phone']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2 or len(name) > 100:
            raise forms.ValidationError("Name must be between 2 and 100 characters.")
        return name

    def clean_phone(self):
        raw_phone = self.cleaned_data.get('phone', '')
        # Strip spaces, brackets, parentheses, and dashes
        cleaned = re.sub(r'[\s\(\)\-]', '', raw_phone)
        # Must be +998 followed by exactly 9 digits
        if not re.fullmatch(r'\+998\d{9}', cleaned):
            raise forms.ValidationError("Phone number must be +998 followed by exactly 9 digits.")
        return cleaned
