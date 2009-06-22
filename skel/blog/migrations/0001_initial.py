
from south.db import db
from django.db import models
from skel.blog.models import *

class Migration:

    depends_on = (
        ('categories', '0001_initial'),
    )
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('blog_entries', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=255)),
            ('public', models.BooleanField(default=True)),
            ('author', models.ForeignKey(orm['auth.User'])),
            ('tags', TagField(blank=True)),
            ('media', models.ForeignKey(orm['massmedia.Collection'], null=True, blank=True)),
            ('slug', models.SlugField(unique_for_date='published')),
            ('updated', models.DateTimeField(auto_now=True)),
            ('published', models.DateTimeField(default=datetime.datetime.now)),
            ('summary_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('summary_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('body_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('body_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('summary', MarkupEditorField(blank=True)),
            ('body', MarkupEditorField()),
        ))
        db.send_create_signal('blog', ['Entry'])
        
        # Adding ManyToManyField 'Entry.categories'
        db.create_table('blog_entries_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm.Entry, null=False)),
            ('category', models.ForeignKey(orm['categories.Category'], null=False))
        ))
        
        # Adding ManyToManyField 'Entry.sites'
        db.create_table('blog_entries_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm.Entry, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('blog_entries')
        
        # Dropping ManyToManyField 'Entry.categories'
        db.delete_table('blog_entries_categories')
        
        # Dropping ManyToManyField 'Entry.sites'
        db.delete_table('blog_entries_sites')
        
    

    models = {
        'blog.entry': {
            'Meta': {'ordering': "('-published',)", 'db_table': "'blog_entries'", 'get_latest_by': "'published'"},
            'author': ('models.ForeignKey', ["orm['auth.User']"], {}),
            'body': ('MarkupEditorField', [], {}),
            'body_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'body_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'categories': ('models.ManyToManyField', ["orm['categories.Category']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media': ('models.ForeignKey', ["orm['massmedia.Collection']"], {'null': 'True', 'blank': 'True'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'published': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {}),
            'slug': ('models.SlugField', [], {'unique_for_date': "'published'"}),
            'summary': ('MarkupEditorField', [], {'blank': 'True'}),
            'summary_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'summary_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'tags': ('TagField', [], {'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'updated': ('models.DateTimeField', [], {'auto_now': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'categories.category': {
            'Meta': {'ordering': "('slug',)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'massmedia.collection': {
            'Meta': {'ordering': "['-creation_date']", 'get_latest_by': "'creation_date'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['blog']
