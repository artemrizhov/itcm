
from south.db import db
from django.db import models
from cms.plugins.snippet.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PublicSnippetPtr'
        db.create_table('snippet_publicsnippetptr', (
            ('snippet', orm['snippet.publicsnippetptr:snippet']),
            ('mark_delete', orm['snippet.publicsnippetptr:mark_delete']),
            ('publiccmsplugin_ptr', orm['snippet.publicsnippetptr:publiccmsplugin_ptr']),
        ))
        db.send_create_signal('snippet', ['PublicSnippetPtr'])
        
        # Adding field 'SnippetPtr.public'
        db.add_column('snippet_snippetptr', 'public', orm['snippet.snippetptr:public'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PublicSnippetPtr'
        db.delete_table('snippet_publicsnippetptr')
        
        # Deleting field 'SnippetPtr.public'
        db.delete_column('snippet_snippetptr', 'public_id')
        
    
    
    models = {
        'snippet.snippet': {
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'cms.publiccmsplugin': {
            '_stub': True,
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'})
        },
        'cms.publicpage': {
            '_stub': True,
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'})
        },
        'cms.cmsplugin': {
            '_stub': True,
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'})
        },
        'snippet.publicsnippetptr': {
            'mark_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'publiccmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.PublicCMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['snippet.Snippet']"})
        },
        'snippet.snippetptr': {
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'public': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'origin'", 'unique': 'True', 'null': 'True', 'to': "orm['snippet.PublicSnippetPtr']"}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['snippet.Snippet']"})
        },
        'cms.page': {
            '_stub': True,
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['snippet']
