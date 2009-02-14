from django.db import models
#from crop.fields import ThumbnailField

class Thumbnail(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='img/thumbnails/', blank=True, width_field='width', height_field='height')
    width = models.PositiveIntegerField(blank=True)
    height = models.PositiveIntegerField(blank=True)

    @property
    def url(self):
        return self.thumbnail.url