
from south.db import db
from django.db import models
from skel.portfolio.models import *

class Migration:

    depends_on = (
        ('categories', '0001_initial'),
    )
        
    def forwards(self, orm):
        
        # Adding model 'Project'
        db.create_table('portfolio_project', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=255)),
            ('public', models.BooleanField(default=True)),
            ('tags', TagField(blank=True)),
            ('media', models.ForeignKey(orm['massmedia.Collection'], null=True, blank=True)),
            ('slug', models.SlugField(unique=True)),
            ('updated', models.DateTimeField(auto_now=True)),
            ('summary_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('summary_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('published', models.DateTimeField(default=datetime.datetime.now)),
            ('description_markup', models.CharField(null=True, blank=True, max_length=255)),
            ('description_rendered', models.TextField(null=True, blank=True, editable=False)),
            ('summary', MarkupEditorField(blank=True)),
            ('description', MarkupEditorField()),
            ('started', models.DateTimeField(null=True, blank=True)),
            ('finished', models.DateTimeField(null=True, blank=True)),
            ('status', models.CharField(max_length=255, blank=True)),
            ('client', models.ForeignKey(orm.Client, null=True, blank=True)),
            ('role', models.CharField(max_length=255, blank=True)),
            ('url', models.URLField(verify_exists=True, blank=True)),
        ))
        db.send_create_signal('portfolio', ['Project'])
        
        # Adding model 'Client'
        db.create_table('portfolio_client', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('slug', models.SlugField(unique=True)),
            ('url', models.URLField(verify_exists=True, blank=True)),
            ('public', models.BooleanField(default=True)),
        ))
        db.send_create_signal('portfolio', ['Client'])
        
        # Adding model 'Testimonial'
        db.create_table('portfolio_testimonial', (
            ('id', models.AutoField(primary_key=True)),
            ('quotee', models.CharField(max_length=255)),
            ('quote', models.TextField()),
            ('url', models.URLField(verify_exists=True, blank=True)),
            ('client', models.ForeignKey(orm.Client, null=True, blank=True)),
            ('public', models.BooleanField(default=True)),
        ))
        db.send_create_signal('portfolio', ['Testimonial'])
        
        # Adding ManyToManyField 'Project.testimonials'
        db.create_table('portfolio_project_testimonials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm.Project, null=False)),
            ('testimonial', models.ForeignKey(orm.Testimonial, null=False))
        ))
        
        # Adding ManyToManyField 'Project.sites'
        db.create_table('portfolio_project_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm.Project, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
        # Adding ManyToManyField 'Project.categories'
        db.create_table('portfolio_project_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm.Project, null=False)),
            ('category', models.ForeignKey(orm['categories.Category'], null=False))
        ))
        
        # Adding ManyToManyField 'Project.maintainers'
        db.create_table('portfolio_project_maintainers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm.Project, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'Testimonial.sites'
        db.create_table('portfolio_testimonial_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testimonial', models.ForeignKey(orm.Testimonial, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
        # Adding ManyToManyField 'Client.sites'
        db.create_table('portfolio_client_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm.Client, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
        # Adding ManyToManyField 'Project.contributors'
        db.create_table('portfolio_project_contributors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm.Project, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Project'
        db.delete_table('portfolio_project')
        
        # Deleting model 'Client'
        db.delete_table('portfolio_client')
        
        # Deleting model 'Testimonial'
        db.delete_table('portfolio_testimonial')
        
        # Dropping ManyToManyField 'Project.testimonials'
        db.delete_table('portfolio_project_testimonials')
        
        # Dropping ManyToManyField 'Project.sites'
        db.delete_table('portfolio_project_sites')
        
        # Dropping ManyToManyField 'Project.categories'
        db.delete_table('portfolio_project_categories')
        
        # Dropping ManyToManyField 'Project.maintainers'
        db.delete_table('portfolio_project_maintainers')
        
        # Dropping ManyToManyField 'Testimonial.sites'
        db.delete_table('portfolio_testimonial_sites')
        
        # Dropping ManyToManyField 'Client.sites'
        db.delete_table('portfolio_client_sites')
        
        # Dropping ManyToManyField 'Project.contributors'
        db.delete_table('portfolio_project_contributors')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'portfolio.testimonial': {
            'client': ('models.ForeignKey', ["orm['portfolio.Client']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'quote': ('models.TextField', [], {}),
            'quotee': ('models.CharField', [], {'max_length': '255'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {}),
            'url': ('models.URLField', [], {'verify_exists': 'True', 'blank': 'True'})
        },
        'massmedia.collection': {
            'Meta': {'ordering': "['-creation_date']", 'get_latest_by': "'creation_date'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'portfolio.project': {
            'Meta': {'ordering': "('-published',)", 'get_latest_by': "'published'"},
            'categories': ('models.ManyToManyField', ["orm['categories.Category']"], {'null': 'True', 'blank': 'True'}),
            'client': ('models.ForeignKey', ["orm['portfolio.Client']"], {'null': 'True', 'blank': 'True'}),
            'contributors': ('models.ManyToManyField', ["orm['auth.User']"], {'related_name': "'projects_contributes_to'", 'null': 'True', 'blank': 'True'}),
            'description': ('MarkupEditorField', [], {}),
            'description_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'description_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'finished': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'maintainers': ('models.ManyToManyField', ["orm['auth.User']"], {'related_name': "'projects_maintained'", 'null': 'True', 'blank': 'True'}),
            'media': ('models.ForeignKey', ["orm['massmedia.Collection']"], {'null': 'True', 'blank': 'True'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'published': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'role': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {}),
            'slug': ('models.SlugField', [], {'unique': 'True'}),
            'started': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'summary': ('MarkupEditorField', [], {'blank': 'True'}),
            'summary_markup': ('models.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'summary_rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True', 'editable': 'False'}),
            'tags': ('TagField', [], {'blank': 'True'}),
            'testimonials': ('models.ManyToManyField', ["orm['portfolio.Testimonial']"], {'null': 'True', 'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'updated': ('models.DateTimeField', [], {'auto_now': 'True'}),
            'url': ('models.URLField', [], {'verify_exists': 'True', 'blank': 'True'})
        },
        'categories.category': {
            'Meta': {'ordering': "('slug',)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'portfolio.client': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {}),
            'slug': ('models.SlugField', [], {'unique': 'True'}),
            'url': ('models.URLField', [], {'verify_exists': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['portfolio']
