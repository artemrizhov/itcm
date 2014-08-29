from django.conf import settings
from django.db import models

from cms.models import CMSPlugin


class PublicationList(CMSPlugin):
    """A list of references to published papers/books etc
    """
    def __unicode__(self):
        return u" | ".join(map(unicode,list(self.publication_set.all())))

    def copy_relations(self, old_instance):
        for publication in old_instance.publication_set.all():
            new_publication = Publication()
            new_publication.publicationlist = self
            new_publication.text = publication.text
            new_publication.link = publication.link
            new_publication.pdf = publication.pdf
            new_publication.bibtex = publication.bibtex
            new_publication.save()
        
class Publication(models.Model):
    """
    A published paper/book etc
    """
    publicationlist = models.ForeignKey(PublicationList)
    text = models.TextField()
    link = models.URLField(blank=True, null=True)
    pdf = models.FileField(upload_to=lambda p, *args: CMSPlugin.get_media_path(p.publicationlist,*args), blank=True, null=True)
    bibtex = models.TextField(blank=True)

    def __unicode__(self):
        return self.text

if 'reversion' in settings.INSTALLED_APPS:
    import reversion
    reversion.register(PublicationList, follow=["cmsplugin_ptr", "publication_set"])
    reversion.register(Publication)
