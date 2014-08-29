from django.conf import settings
from django.db import models

from cms.models import CMSPlugin
from tinymce.models import HTMLField


class Person(CMSPlugin):
    """
    A person's details
    """

    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to=CMSPlugin.get_media_path, blank=True)
    role = models.CharField(max_length=256, blank=True)
    phone_no = models.CharField(max_length=256, blank=True)
    email = models.EmailField(max_length=256, blank=True)
    url = models.URLField(max_length=256, blank=True)
    address = models.TextField(max_length=256, blank=True)
    bio = HTMLField(max_length=256, blank=True)

    def __unicode__(self):
        return self.name

if 'reversion' in settings.INSTALLED_APPS:
    import reversion
    reversion.register(Person)
