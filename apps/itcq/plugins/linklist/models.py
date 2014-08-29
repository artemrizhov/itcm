from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, Page


class LinkList(CMSPlugin):
    """A list of links to CMS pages
    """
    def __unicode__(self):
        return u" | ".join(map(unicode,list(self.linklistlink_set.all())))

    def copy_relations(self, old_instance):
        for link in old_instance.linklistlink_set.all():
            new_link = LinkListLink()
            new_link.linklist = self
            new_link.link_text = link.link_text
            new_link.description = link.description
            new_link.page_link = link.page_link
            new_link.url = link.url
            new_link.save()


class LinkListLink(models.Model):
    """
    A link to an other page or to an external website
    """

    linklist = models.ForeignKey(LinkList)
    link_text = models.CharField(_("name"), max_length=256, help_text="The text of the link itself")
    description = models.CharField(_("description"), max_length=256, blank=True, help_text="(optional) A small piece of text to follow the link.")
    page_link = models.ForeignKey(Page, verbose_name=_("page"), blank=True, null=True, help_text=_("Select a page to link to here (or leave it blank and enter a URL below)."))
    url = models.URLField(_("link"), blank=True, null=True, help_text="Enter a URL here if the link is to be to an external site.")

    def get_link_url(self):
        if self.page_link:
            return self.page_link.get_absolute_url()
        else:
            return self.url

    def __unicode__(self):
        return self.link_text

if 'reversion' in settings.INSTALLED_APPS:
    import reversion
    reversion.register(LinkList, follow=["cmsplugin_ptr", "linklistlink_set"])
    reversion.register(LinkListLink)
