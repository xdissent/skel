
from south.db import db
from django.db import models
from skel.categories.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('categories_category', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
            ('description_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('description_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('slug', models.SlugField(unique=True, db_index=True)),
            ('description', MarkupEditorField(blank=True)),
            ('public', models.BooleanField(default=True)),
        ))
        db.send_create_signal('categories', ['Category'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('categories_category')
        
    
    
    models = {
        'categories.category': {
            'Meta': {'ordering': "('slug',)"},
            'description': ('MarkupEditorField', [], {'blank': 'True'}),
            'description_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'description_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['categories']
