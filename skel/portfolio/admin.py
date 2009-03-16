from django.contrib import admin
from skel.portfolio import settings
from skel.portfolio.models import Project, Client, Testimonial

class ClientAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'url',
            ),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
            ),
        }),
    )


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1


project_fields = [
    'title', 
    'public',
    'maintainers',
    'contributors',
    'client',
    'started',
    'finished',
    'status',
    'role',
    'url',
    'sites',
    'summary',
    'description',
]


project_list_filter = ('public', 'sites')


if settings.PORTFOLIO_TAGS_ENABLED:
    project_fields.append('tags')
    project_list_filter += ('tags',)


if settings.PORTFOLIO_CATEGORIES_ENABLED:
    project_fields.append('categories')
    project_list_filter += ('categories',)


if settings.PORTFOLIO_MARKUP_ENABLED:
    for field in ('summary', 'description'):
        project_fields.insert(project_fields.index(field) + 1, field + '_markup')
        

if settings.PORTFOLIO_MEDIA_ENABLED:
    project_fields.append('media')


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': project_fields
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'published',
            )
        }),
    )
    list_display = ('published', 'title', 'public',)
    list_filter = project_list_filter
    search_fields = ['title', 'description', 'summary']
    model_admin_manager = Project.admin_manager
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['contributors'].initial = (request.user.pk,)
            form.base_fields['maintainers'].initial = (request.user.pk,)
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(Project, ProjectAdmin)