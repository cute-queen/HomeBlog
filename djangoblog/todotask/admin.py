
from multiprocessing import parent_process
from django.contrib import admin
from .models import Todo, Task
from django.db.models.signals import post_save
from django.dispatch import receiver


# Update task progress
def update_task_progress(task):
    todos = Todo.objects.filter(parent_task = task)
    finish_num = 0
    for todo in todos:
        if todo.progress_status == 'f':
            finish_num += 1
    total_num = len(todos)
    if total_num > 0 and finish_num <= total_num:
        task.progress = int(finish_num / len(todos) * 100)
    else:
        task.progress = 100
    task.save()


class TodoInline(admin.TabularInline):
    model = Todo
    fk_name = 'parent_task'
    list_display = ('title', 'progress_status')
    fields = ('title', 'remark', 'progress_status')


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'progress_status')
    fields = ('title', 'remark', 'progress_status')
"""
 def save_model(self, request, obj, form, change):
        state = super(TodoAdmin, self).save_model(request, obj, form, change)
        task = obj.parent_task
        if task:
            update_task_progress(task)
        return state
"""

class TaskAdmin(admin.ModelAdmin):
    inlines = [TodoInline]
    list_display = ('title', 'progress')


@receiver(post_save, sender=Todo)
def post_todo_update(sender, **kwargs):
    instance = kwargs['instance']
    task = instance.parent_task
    if task:
        update_task_progress(task)