from pydoc import describe
from pyexpat import model
from statistics import mode
from django.db import models
from django.utils.timezone import now
from djangoblog.utils import cache_decorator, cache

# Create your models here.

class TodoTask(models.Model):
    title = models.CharField('标题', max_length=200, unique=False)
    remark = models.TextField('备注')
    parent_task = models.ForeignKey(
        'self',
        verbose_name="父级任务",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    percent = models.IntegerField(default=0, verbose_name="进度")
    c_time = models.DateTimeField(
        '创建时间', blank=False, null=False, default=now)

    class Meta:
        ordering = ['-c_time']
        verbose_name = "任务"
        verbose_name_plural = verbose_name

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        """
        递归获得分类目录的父级
        :return:
        """
        tasks = []

        def parse(task):
            tasks.append(task)
            if task.parent_task:
                parse(task.parent_task)

        parse(self)
        return tasks

    @cache_decorator(60 * 60 * 10)
    def get_sub_categorys(self):
        """
        获得当前分类目录所有子集
        :return:
        """
        tasks = []
        all_tasks = TodoTask.objects.all()

        def parse(task):
            if task not in tasks:
                tasks.append(task)
            childs = all_tasks.filter(parent_task=task)
            for child in childs:
                if task not in tasks:
                    tasks.append(child)
                parse(child)

        parse(self)
        return tasks

    def __str__(self):
        return self.title