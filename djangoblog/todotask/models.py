from pydoc import describe
from pyexpat import model
from statistics import mode
from django.db import models
from django.utils.timezone import now

# Create your models here.

class BaseTodo(models.Model):
    title = models.CharField('标题', max_length=200, unique=False)
    remark = models.TextField('备注')
    create_time = models.DateTimeField(
        '发布时间', blank=False, null=False, default=now)

class Todo(models.Model):
    TODO_STATUS = (
        ('f', '完成'),
        ('n', '未完成'),
    )
    title = models.CharField('标题', max_length=200, unique=False)
    remark = models.TextField('备注')

class Task(models.Model):
    title = models.CharField('标题', max_length=200, unique=False)
    remark = models.TextField('备注')
