import six
from django.utils.text import Truncator
from django.utils.functional import allow_lazy
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.html import strip_tags

from cms.models import CMSPlugin, Page
from djangocms_text_ckeditor.models import AbstractText
from djangocms_text_ckeditor.utils import (
    plugin_to_tag as plugin_admin_html_to_tags,
    plugin_tags_to_user_html as plugin_tags_to_admin_html)


def truncate_words(s, num, end_text='...'):
    truncate = end_text and ' %s' % end_text or ''
    return Truncator(s).words(num, truncate=truncate)
truncate_words = allow_lazy(truncate_words, six.text_type)


class ResearchAreaPreview(AbstractText):
    heading = models.CharField(_("heading"), max_length=256)
    image = models.ImageField(_("image"), upload_to=CMSPlugin.get_media_path, blank=True, null=True)
    more_link = models.ForeignKey(Page, verbose_name=_("Read more link"), help_text=_("Image, heading and the link at the bottom will all link to this page."), blank=True, null=True)
    
    def _set_body_admin(self, text):
        self.body = plugin_admin_html_to_tags(text)

    def _get_body_admin(self):
        return plugin_tags_to_admin_html(self.body)

    body_for_admin = property(_get_body_admin, _set_body_admin, None,
                              """
                              body attribute, but with transformations
                              applied to allow editing in the
                              admin. Read/write.
                              """)

    
    def __unicode__(self):
        return u"%s" % (truncate_words(strip_tags(self.heading), 3)[:30]+"...")

if 'reversion' in settings.INSTALLED_APPS:
    import reversion
    reversion.register(ResearchAreaPreview, follow=["cmsplugin_ptr"])
    

