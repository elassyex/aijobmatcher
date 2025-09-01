from django import forms
from .models import UserProfile

class SkillForm(forms.Form):
    skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your skills separated by commas',
            'class': 'w-full p-2 border rounded'
        }),
        label="Your Skills"
    )
    experience_years = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Years of experience',
            'class': 'w-full p-2 border rounded'
        }),
        label="Years of Experience"
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['skills', 'experience_years']
        widgets = {
            'skills': forms.Textarea(attrs={
                'placeholder': 'Enter your skills as a list or comma-separated',
                'class': 'w-full p-2 border rounded'
            }),
            'experience_years': forms.NumberInput(attrs={
                'placeholder': 'Years of experience',
                'class': 'w-full p-2 border rounded'
            }),
        }
