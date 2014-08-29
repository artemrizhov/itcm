from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _

from .models import Person


class PersonPlugin(CMSPluginBase):
    model = Person
    name = _("Person")
    
    render_template = "itcq/plugins/person.html"
    
    def render(self, context, instance, placeholder):
        context = super(PersonPlugin, self).render(
            context, instance, placeholder)
        context.update({"person": instance})
        return context
    
plugin_pool.register_plugin(PersonPlugin)
