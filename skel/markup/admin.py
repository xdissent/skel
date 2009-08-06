from django.contrib import admin
from skel.markup.forms import markedup_modelform_factory

class MarkedUpAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        """Initialize and create form for the model."""
        super(MarkedUpAdmin, self).__init__(*args, **kwargs)
        self.form = markedup_modelform_factory(self.model)