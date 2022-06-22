from django.contrib import admin

# Register your models here.

class AppLoginSessionAdmin(admin.ModelAdmin):
    list_display = ('author', 'last_operate_time')

class AppImageCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_time')

class AppUploadImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'upload_time')