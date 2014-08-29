from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import LinkList, LinkListLink
from .forms import LinkForm


class LinkInlineAdmin(admin.StackedInline):
    model = LinkListLink
    form = LinkForm

class LinkListPlugin(CMSPluginBase):
    model = LinkList
    name = _("Links")
    
    inlines = [
        LinkInlineAdmin,
    ]
    
    render_template = "itcq/plugins/linklist.html"
    
    def render(self, context, instance, placeholder):
        context = super(LinkListPlugin, self).render(
            context, instance, placeholder)
        context.update({"links": instance.linklistlink_set.all()})
        return context
    
plugin_pool.register_plugin(LinkListPlugin)
