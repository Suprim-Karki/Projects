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

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ('WORK', 'Work Experience'),
        ('EDU', 'Education'),
    ]
    
    type = models.CharField(max_length=4, choices=EXPERIENCE_TYPES)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['-end_date', '-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"