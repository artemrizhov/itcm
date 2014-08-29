# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from reversion.models import has_int_pk, Version
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    depends_on = (
        ("reversion", "0003_auto__add_field_version_object_id_int"),
    )

    needed_by = (
        ("reversion", "0004_populate_object_id_int"),
    )

    def forwards(self, orm):
        "Write your forwards methods here."
        for version in Version.objects.filter(object_id_int__isnull=True).iterator():
            try:
                content_type = ContentType.objects.get_for_id(version.content_type_id)
            except AttributeError:
                version.delete()  # This version refers to a content type that doesn't exist any more.
                continue
            model = content_type.model_class()
            if model is None:
                version.delete()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'itcq.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['itcq']
    symmetrical = True
