from django import forms
from cms.models import Page

from .models import LinkListLink


class LinkForm(forms.ModelForm):
    class Meta:
        model = LinkListLink

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['page_link'].queryset = Page.objects.drafts()

