from django.db import models
from django.db import models
from django.core.validators import URLValidator

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='projects/')
    technologies = models.CharField(max_length=200)
    project_url = models.URLField(validators=[URLValidator()], blank=True)
    github_url = models.URLField(validators=[URLValidator()], blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

