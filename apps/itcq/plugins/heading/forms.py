from django.forms.models import ModelForm
from cms.models import Page

from .models import SectionHeading


class HeadingForm(ModelForm):
    class Meta:
        model = SectionHeading

    def __init__(self, *args, **kwargs):
        super(HeadingForm, self).__init__(*args, **kwargs)
        self.fields['link'].queryset = Page.objects.drafts()
