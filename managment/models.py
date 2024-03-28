from django.db import models

class Book(models.Model):
  title = models.CharField(max_length=255, unique=True)
  authors = models.CharField(max_length=255)
  publication_date = models.DateField(blank=True, null=True)
  isbn = models.CharField(max_length=13, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.title