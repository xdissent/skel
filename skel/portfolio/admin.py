from django.contrib import admin
from django.conf import settings
from skel.portfolio.models import Project, Client, Section, SectionMembership, Testimonial, Image, ImageOwnership

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
    
    
class SectionInline(admin.TabularInline):
    model = SectionMembership
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'order',
            ),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
            ),
        }),
    )
    inlines = [SectionInline]


class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'original',
            ),
        }),
    )
    

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    

class ImageInline(admin.TabularInline):
    model = ImageOwnership
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'content',
                'tags',
                'public',
                'sites',
                'client',
                'role',
                'url',
            ),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'content_html',
                'slug',
                'published',
            ),
        }),
    )
    list_display = ('published', 'title', 'public')
    list_filter = ('public', 'sites', 'client')
    search_fields = ['title', 'content']
    inlines = [TestimonialInline, SectionInline, ImageInline]    
    model_admin_manager = Project.admin_manager
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(Project, ProjectAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Image, ImageAdmin)