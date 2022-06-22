from django.conf.urls import url
from django.urls import path

from . import views

app_name = "apprequest"

urlpatterns = [
    url(r'^app_login/$',
        views.app_login,
        name='app_login'),
    url(r'^verify_session/$',
        views.app_seesion_valid,
        name="verify_session"),
    url(r'^get_categorys/$',
        views.app_get_categorys,
        name="app_get_categorys"),
    url(r'^get_image_categorys/$',
        views.app_get_image_categorys,
        name='get_image_categorys'),
    url(r'^upload_image/$',
        views.image_upload,
        name='image_upload'),
    url('^delete_image/$',
        views.delete_image,
        name='delete_image'),
    url('^upload_blog/$',
        views.upload_blog,
        name='upload_blog'),
    url(r'^app_test/$',
        views.app_test,
        name='app_test'),
]