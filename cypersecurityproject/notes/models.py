from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  note = models.CharField(max_length=250)

  def __str__(self):
    return self.note
