from django.db import models
from skel import markup, categories
import tagging

class Quote(models.Model):
    quotee = models.CharField(max_length=255)
    quote = models.TextField()
    tags = tagging.fields.TagField()

markup.register(Quote)
categories.register(Quote)
# tagging.register(Quote)