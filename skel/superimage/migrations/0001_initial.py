
from south.db import db
from django.db import models
from skel.superimage.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Thumbnail'
        db.create_table('superimage_thumbnail', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=255)),
            ('thumbnail', models.ImageField(height_field='height', width_field='width', blank=True)),
            ('width', models.PositiveIntegerField(null=True, editable=False, blank=True)),
            ('height', models.PositiveIntegerField(null=True, editable=False, blank=True)),
            ('x1', models.PositiveIntegerField(null=True, editable=False, blank=True)),
            ('x2', models.PositiveIntegerField(null=True, editable=False, blank=True)),
            ('y1', models.PositiveIntegerField(null=True, editable=False, blank=True)),
            ('y2', models.PositiveIntegerField(null=True, editable=False, blank=True)),
        ))
        db.send_create_signal('superimage', ['Thumbnail'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Thumbnail'
        db.delete_table('superimage_thumbnail')
        
    
    
    models = {
        'superimage.thumbnail': {
            'height': ('models.PositiveIntegerField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'thumbnail': ('models.ImageField', [], {'height_field': "'height'", 'width_field': "'width'", 'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'width': ('models.PositiveIntegerField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'x1': ('models.PositiveIntegerField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'x2': ('models.PositiveIntegerField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'y1': ('models.PositiveIntegerField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'y2': ('models.PositiveIntegerField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['superimage']
