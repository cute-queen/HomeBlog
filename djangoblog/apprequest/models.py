from unicodedata import name
from django.db import models
from django.conf import settings
from django.utils.timezone import now
import uuid
import os

# Create your models here.

def get_image_relpath_path(names, fext, count=0):
    blocks = names[-1].split('_')
    try:
        num = int(blocks[-1])
    except:
        num = -1
    if count > 0:
        if num > 0:
            blocks[-1] = str(count)
        else:
            blocks.append(str(count))
    names[-1] = '_'.join(blocks)
    fname = '{name}.{ext}'.format(name='_'.join(names), ext=fext)
    return 'app_update_image/{name}'.format(name=fname)

def get_file_exist(relpath):
    fpath = os.path.join(settings.MEDIA_ROOT, relpath)
    return os.path.isfile(fpath)

def generate_image_path(instance, filename):
    fext = filename.split('.')[-1]
    names = filename.split('.')[:-1]
    count = 0
    fname = get_image_relpath_path(names, fext)
    file_exist = get_file_exist(fname)
    while file_exist:
        count += 1
        fname = get_image_relpath_path(names, fext, count)
        file_exist = get_file_exist(fname)
    return fname

class AppLoginSession(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作者',
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    session = models.CharField('密钥', max_length=100)
    created_time = models.DateTimeField('创建时间', default=now)
    last_operate_time = models.DateTimeField('最近操作时间', default=now)

    class Meta:
        ordering = ['-created_time']
        verbose_name = "App登录"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'


class AppImageCategory(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', default=now)
    title = models.CharField('类型', max_length=200, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['created_time']
        verbose_name = "App上传图片分类"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'



class AppUploadImage(models.Model):
    id = models.AutoField(primary_key=True)
    upload_time = models.DateTimeField('上传时间', default=now)
    category = models.ForeignKey(
        AppImageCategory,
        verbose_name='所属分类',
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    
    image = models.ImageField('图片', null=True, upload_to=generate_image_path)

    def __str__(self):
        return self.image.url

    class Meta:
        ordering = ['upload_time']
        verbose_name = "App上传图片"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'