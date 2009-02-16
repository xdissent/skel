from django.db import models
#from crop.fields import ThumbnailField

class Thumbnail(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, width_field='width', height_field='height')
    width = models.PositiveIntegerField(blank=True, null=True, editable=False)
    height = models.PositiveIntegerField(blank=True, null=True, editable=False)
    x1 = models.PositiveIntegerField(blank=True, null=True, editable=False)
    x2 = models.PositiveIntegerField(blank=True, null=True, editable=False)
    y1 = models.PositiveIntegerField(blank=True, null=True, editable=False)
    y2 = models.PositiveIntegerField(blank=True, null=True, editable=False)
    

    @property
    def url(self):
        return self.thumbnail.url