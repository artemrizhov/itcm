from django import forms
from .models import ITCQFlash

class FlashForm(forms.ModelForm):
    
    class Meta:
        model = ITCQFlash
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
