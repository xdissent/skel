from django.contrib import admin
from django import forms, template
from django.forms.formsets import all_valid
from django.forms.models import modelform_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import widgets
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.functional import update_wrapper
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

class ModelAdmin(admin.ModelAdmin):
    def manager(self, request):
        if not hasattr(self, 'model_admin_manager'):
            self.model_admin_manager = self.model._default_manager
        return self.model_admin_manager
        
    def queryset(self, request):
        qs = self.manager(request).get_query_set()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
        
    def change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta
        
        try:
            obj = self.manager(request).get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None
        
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        
        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        
        if request.method == 'POST' and request.POST.has_key("_saveasnew"):
            return self.add_view(request, form_url='../../add/')
        
        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            for FormSet in self.get_formsets(request, new_object):
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object)
                formsets.append(formset)
            
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)
                
                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)
        
        else:
            form = ModelForm(instance=obj)
            for FormSet in self.get_formsets(request, obj):
                formset = FormSet(instance=obj)
                formsets.append(formset)
        
        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj), self.prepopulated_fields)
        media = self.media + adminForm.media
        
        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media
        
        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)
    change_view = transaction.commit_on_success(change_view)
    
    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label
        
        try:
            obj = self.manager(request).get(pk=unquote(object_id))
        except self.model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None
        
        if not self.has_delete_permission(request, obj):
            raise PermissionDenied
        
        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        
        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        deleted_objects = [mark_safe(u'%s: <a href="../../%s/">%s</a>' % (escape(force_unicode(capfirst(opts.verbose_name))), object_id, escape(obj))), []]
        perms_needed = set()
        get_deleted_objects(deleted_objects, perms_needed, request.user, obj, opts, 1, self.admin_site)
        
        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            obj.delete()
            
            self.log_deletion(request, obj, obj_display)
            self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
            
            if not self.has_change_permission(request, None):
                return HttpResponseRedirect("../../../../")
            return HttpResponseRedirect("../../")
        
        context = {
            "title": _("Are you sure?"),
            "object_name": force_unicode(opts.verbose_name),
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, context_instance=template.RequestContext(request))
        
    def save_model(self, request, obj, form, change):
        obj.save(force_update=change)
