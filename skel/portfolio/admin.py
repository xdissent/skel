from django.contrib import admin
from django.conf import settings
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


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'tags',
                'categories',
                'public',
                'sites',
                'client',
                'role',
                'url',
                'description',
                'description_markup',
                'summary',
                'summary_markup',
                'images',
            ),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'published',
            ),
        }),
    )
    list_display = ('published', 'title', 'client', 'public')
    list_filter = ('public', 'sites', 'client', 'categories', 'tags')
    search_fields = ['title', 'description']
    inlines = [TestimonialInline,]    
    model_admin_manager = Project.admin_manager
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(Project, ProjectAdmin)
admin.site.register(Client, ClientAdmin)