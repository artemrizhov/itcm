from django.forms.models import ModelForm
from cms.models import Page

from .models import ResearchAreaPreview


class ResearchAreaPreviewForm(ModelForm):
    class Meta:
        model = ResearchAreaPreview
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(ResearchAreaPreviewForm, self).__init__(*args, **kwargs)
        self.fields['more_link'].queryset = Page.objects.drafts()
