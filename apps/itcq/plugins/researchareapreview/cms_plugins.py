from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.cms_plugins import TextPlugin

from .models import ResearchAreaPreview
from .forms import ResearchAreaPreviewForm


class ResearchAreaPreviewPlugin(TextPlugin):
    model = ResearchAreaPreview
    name = "Research Area Preview"
    form = ResearchAreaPreviewForm
    render_template = "cms/plugins/researchareapreview.html"

    def render(self, context, instance, placeholder):
        context = super(ResearchAreaPreviewPlugin, self).render(context, instance, placeholder)
        context.update({
            'instance': instance,
        })
        return context

plugin_pool.register_plugin(ResearchAreaPreviewPlugin)
