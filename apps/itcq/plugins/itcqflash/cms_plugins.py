from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .forms import FlashForm
from .models import ITCQFlash


class ITCQFlashPlugin(CMSPluginBase):
    model = ITCQFlash
    name = _("Flash (with caption)")
    form = FlashForm
    
    render_template = "itcq/plugins/itcqflash.html"
    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder':placeholder,
        })
        return context
    
plugin_pool.register_plugin(ITCQFlashPlugin)
