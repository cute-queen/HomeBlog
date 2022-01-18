from django.contrib import admin
from .models import TodoTask

# Register your models here.

class TodoTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'remark', 'parent_task', 'percent')
    exclude = ('c_time')