from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class MarkedUpItem(models.Model):
    """A model to store rendered markup for a field on another model."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    source_field = models.CharField(max_length=50, blank=True)
    source_hash = models.CharField(max_length=32, blank=True)
    rendered = models.TextField(blank=True)
    engine_name = models.CharField(max_length=50, blank=True)
    
    class Meta:
        pass
        
    @property
    def needs_update(self):
        return True
    
    @property
    def render_options(self):
        return {}
        
    def get_engine(self):
        from skel.markup.engines import registered_engines
        return registered_engines[self.engine_name]()
    
    def set_engine(self, value):
        if not isinstance(value, basestring):
            value = value.name
        self.engine_name = value
    engine = property(get_engine, set_engine)

    def render(self, source=None):
        if source is None:
            source = getattr(self.content_object, self.source_field, '')
        self.rendered = self.engine.render(source, self.render_options)