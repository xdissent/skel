
from south.db import db
from django.db import models
from skel.accounts.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'], unique=True)),
            ('bio_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('bio_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('url', models.URLField(verify_exists=True, blank=True)),
            ('bio', MarkupEditorField(blank=True)),
            ('public', models.BooleanField(default=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])
        
        # Adding ManyToManyField 'UserProfile.sites'
        db.create_table('accounts_userprofile_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm.UserProfile, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')
        
        # Dropping ManyToManyField 'UserProfile.sites'
        db.delete_table('accounts_userprofile_sites')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.userprofile': {
            'bio': ('MarkupEditorField', [], {'blank': 'True'}),
            'bio_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'bio_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {}),
            'url': ('models.URLField', [], {'verify_exists': 'True', 'blank': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'unique': 'True'})
        }
    }
    
    complete_apps = ['accounts']
