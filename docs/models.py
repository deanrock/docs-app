import re
from django.contrib.auth.models import User
from django.db import models
import unidecode


def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

def get_url(model, name):
    url = slugify(name).strip('-')

    i = 1

    url_new = url

    while True:
        if model.objects.filter(url = url_new).first():
            url_new = url+str(i)
            i = i+1
        else:
          break

    return url

class Project(models.Model):
    added_at = models.DateTimeField()
    added_by = models.ForeignKey(User)

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

class Page(models.Model):
    added_at = models.DateTimeField()
    added_by = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    deleted = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

class Version(models.Model):
    added_at = models.DateTimeField()
    added_by = models.ForeignKey(User)
    page = models.ForeignKey(Page)

    title = models.CharField(max_length=255)
    content = models.TextField()
