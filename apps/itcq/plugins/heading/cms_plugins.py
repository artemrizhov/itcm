from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import SectionHeading
from .forms import HeadingForm


class HeadingPlugin(CMSPluginBase):
    model = SectionHeading
    name = _("Section Heading")
    render_template = "itcq/plugins/heading.html"
    form = HeadingForm
    
    def render(self, context, instance, placeholder):
        context = super(HeadingPlugin, self).render(context, instance, placeholder)
        context.update({"heading": instance.heading, "level": instance.heading_level, "link": instance.link})
        return context
    
plugin_pool.register_plugin(HeadingPlugin)
