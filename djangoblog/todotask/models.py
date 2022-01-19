from email.policy import default
from pydoc import describe
from pyexpat import model
from statistics import mode
from django.db import models
from django.utils.timezone import now
from djangoblog.utils import cache_decorator, cache

# Create your models here.
class TodoBase(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=200, unique=False)
    remark = models.TextField('备注', null=True, blank=True)
    
    c_time = models.DateTimeField(
        '创建时间', blank=False, null=False, default=now)
    
    class Meta:
        ordering = ['-c_time']

    def __str__(self):
        return self.title


class Task(TodoBase):    
    progress = models.IntegerField(default=0, verbose_name="进度")

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = verbose_name

class Todo(TodoBase):
    PROGRESS_CHOICES = (
        ('f', '完成'),
        ('n', '未完成'),
    )
    
    parent_task = models.ForeignKey(
        Task, 
        verbose_name='所属任务', 
        null=True,blank=True,
        related_name = 'todos',
        on_delete=models.CASCADE)

    progress_status = models.CharField(
        '完成情况',
        max_length=1,
        choices=PROGRESS_CHOICES,
        default='n')
    
    task_order = models.IntegerField(
        '任务排序', blank=False, null=False, default=0)

    class Meta:
        verbose_name = '待做事项'
        verbose_name_plural = verbose_name