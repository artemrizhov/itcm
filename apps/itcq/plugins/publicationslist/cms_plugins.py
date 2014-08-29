from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import PublicationList, Publication


class PublicationAdmin(admin.StackedInline):
    model = Publication

class PublicationListPlugin(CMSPluginBase):
    model = PublicationList
    name = _("Publications")
    
    inlines = [
        PublicationAdmin,
    ]
    
    render_template = "itcq/plugins/publicationslist.html"
    

    def render(self, context, instance, placeholder):
        context = super(PublicationListPlugin, self).render(
            context, instance, placeholder)
        context.update(
            {"publication_list": instance.publication_set.all().order_by("id")})
        return context
    
plugin_pool.register_plugin(PublicationListPlugin)
