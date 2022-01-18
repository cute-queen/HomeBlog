from pydoc import describe
from statistics import mode
from django.db import models

# Create your models here.

class TodoTask(models.Model):
    title = models.CharField('标题', max_length=200, unique=False)
    remark = models.TextField('备注')