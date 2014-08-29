from django.db import models
import datetime
import os

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=lambda self,f: self.get_media_path(f))
    link = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    def get_media_path(self, filename):
        from cms import settings

        today = datetime.date.today()
        return os.path.join(settings.CMS_PAGE_MEDIA_PATH, str(today.year), str(today.month), str(today.day), filename)
