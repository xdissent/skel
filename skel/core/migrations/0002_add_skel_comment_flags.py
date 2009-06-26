
from south.db import db
from django.db import models
from skel.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'SkelCommentFlag'
        db.create_table('skel_comment_flags', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'], related_name='skel_comment_flags')),
            ('comment', models.ForeignKey(orm.SkelComment, related_name='flags')),
            ('flag', models.CharField('flag', max_length=30, db_index=True)),
            ('flag_date', models.DateTimeField('date', default=None)),
        ))
        db.send_create_signal('core', ['SkelCommentFlag'])
         
        # Creating unique_together for [user, comment, flag] on SkelCommentFlag.
        db.create_unique('skel_comment_flags', ['user_id', 'comment_id', 'flag'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'SkelCommentFlag'
        db.delete_table('skel_comment_flags')
               
        # Deleting unique_together for [user, comment, flag] on SkelCommentFlag.
        db.delete_unique('skel_comment_flags', ['user_id', 'comment_id', 'flag'])
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
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
        },
        'auth.user': {
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'core.skelcommentflag': {
            'Meta': {'unique_together': "[('user','comment','flag')]", 'db_table': "'skel_comment_flags'"},
            'comment': ('models.ForeignKey', ["orm['core.SkelComment']"], {'related_name': "'flags'"}),
            'flag': ('models.CharField', ["'flag'"], {'max_length': '30', 'db_index': 'True'}),
            'flag_date': ('models.DateTimeField', ["'date'"], {'default': 'None'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': "'skel_comment_flags'"})
        }
    }
    
    complete_apps = ['core']
