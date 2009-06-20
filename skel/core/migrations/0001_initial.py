
from south.db import db
from django.db import models
from skel.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'NavigationMenu'
        db.create_table('core_navigationmenu', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=255)),
            ('label', models.CharField(max_length=255)),
            ('url', models.CharField(max_length=255, blank=True)),
            ('public', models.BooleanField(default=True)),
        ))
        db.send_create_signal('core', ['NavigationMenu'])
        
        # Adding model 'SkelComment'
        db.create_table('skel_comments', (
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name="content_type_set_for_%(class)s")),
            ('object_pk', models.TextField(_('object ID'))),
            ('site', models.ForeignKey(orm['sites.Site'])),
            ('comment_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('comment_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('comment', MarkupEditorField()),
            ('user', models.ForeignKey(orm['auth.User'], related_name="%(class)s_comments", null=True, blank=True)),
            ('user_name', models.CharField(max_length=50, blank=True)),
            ('user_email', models.EmailField(blank=True)),
            ('user_url', models.URLField(blank=True)),
            ('submit_date', models.DateTimeField(default=None)),
            ('ip_address', models.IPAddressField(null=True, blank=True)),
            ('is_public', models.BooleanField(default=True)),
            ('is_removed', models.BooleanField(default=False)),
        ))
        db.send_create_signal('core', ['SkelComment'])
        
        # Adding ManyToManyField 'NavigationMenu.children'
        db.create_table('core_navigationmenu_children', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_navigationmenu', models.ForeignKey(orm.NavigationMenu, null=False)),
            ('to_navigationmenu', models.ForeignKey(orm.NavigationMenu, null=False))
        ))
        
        # Adding ManyToManyField 'NavigationMenu.sites'
        db.create_table('core_navigationmenu_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('navigationmenu', models.ForeignKey(orm.NavigationMenu, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'NavigationMenu'
        db.delete_table('core_navigationmenu')
        
        # Deleting model 'SkelComment'
        db.delete_table('skel_comments')
        
        # Dropping ManyToManyField 'NavigationMenu.children'
        db.delete_table('core_navigationmenu_children')
        
        # Dropping ManyToManyField 'NavigationMenu.sites'
        db.delete_table('core_navigationmenu_sites')
        
    
    
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'core.navigationmenu': {
            'children': ('models.ManyToManyField', ["orm['core.NavigationMenu']"], {'related_name': "'parents'", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'max_length': '255'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'url': ('models.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'core.skelcomment': {
            'Meta': {'ordering': "('submit_date',)", 'db_table': "'skel_comments'", 'permissions': "[('can_moderate','Can moderate comments')]"},
            'comment': ('MarkupEditorField', [], {}),
            'comment_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'comment_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': '"content_type_set_for_%(class)s"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('models.IPAddressField', [], {'null': 'True', 'blank': 'True'}),
            'is_public': ('models.BooleanField', [], {'default': 'True'}),
            'is_removed': ('models.BooleanField', [], {'default': 'False'}),
            'object_pk': ('models.TextField', ["_('object ID')"], {}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {}),
            'submit_date': ('models.DateTimeField', [], {'default': 'None'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"%(class)s_comments"', 'null': 'True', 'blank': 'True'}),
            'user_email': ('models.EmailField', [], {'blank': 'True'}),
            'user_name': ('models.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('models.URLField', [], {'blank': 'True'})
        }
    }
    
    complete_apps = ['core']
