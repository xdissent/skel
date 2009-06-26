
from south.db import db
from django.db import models
from skel.quotes.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Quote'
        db.create_table('quotes_quote', (
            ('id', models.AutoField(primary_key=True)),
            ('quotee', models.CharField(max_length=255)),
            ('quote', models.TextField()),
            ('public', models.BooleanField(default=True)),
        ))
        db.send_create_signal('quotes', ['Quote'])
        
        # Adding ManyToManyField 'Quote.sites'
        db.create_table('quotes_quote_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quote', models.ForeignKey(orm.Quote, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Quote'
        db.delete_table('quotes_quote')
        
        # Dropping ManyToManyField 'Quote.sites'
        db.delete_table('quotes_quote_sites')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'quotes.quote': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'quote': ('models.TextField', [], {}),
            'quotee': ('models.CharField', [], {'max_length': '255'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {})
        }
    }
    
    complete_apps = ['quotes']
