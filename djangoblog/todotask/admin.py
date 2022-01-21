
from django.contrib import admin
from .models import Todo, Task

# Register your models here.


class TodoInline(admin.TabularInline):
    model = Todo
    fk_name = 'parent_task'
    list_display = ('title', 'progress_status')


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'progress_status')

class TaskAdmin(admin.ModelAdmin):
    inlines = [TodoInline]
    list_display = ('title', 'progress')


