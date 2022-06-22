
import json
from turtle import title

from .models import AppImageCategory, AppLoginSession, AppUploadImage, generate_image_path
from blog.models import Article, Category

from .utils import AppRequest, get_app_reply, get_userdata

from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import os
from django.core.files import File

from django.conf import settings
from djangoblog.utils import get_blog_setting
from mdeditor.fields import MDTextField
# Create your views here.

DEFAULT_CATEGORY_NAME = "默认"

def convert_to_normal_verifydata(verify_dict):
    if len(verify_dict['username']) < 1 or len(verify_dict['session']) < 1:
        return {
            'username': '',
            'session': ''
        }
    return {
        'username': verify_dict['username'],
        'session': verify_dict['session']
    }

def get_default_image_category():
    default_category = AppImageCategory.objects.filter(title=DEFAULT_CATEGORY_NAME)
    if len(default_category) > 0:
        return default_category[0]
    category = AppImageCategory()
    category.title = DEFAULT_CATEGORY_NAME
    category.save()
    return category

# app登录接口
@csrf_exempt
def app_login(request):
    data = json.loads(request.body)
    username = data.get('username')
    psword = data.get('password')
    reply = {"status": 0, "msg": "未知错误"}
    if username and psword:
        user = authenticate(username=username, password=psword)
        if user:
            session = get_random_string(length=64)
            # 删除所有已经记录的登录密钥
            AppLoginSession.objects.filter(author = user).delete()
            login_session = AppLoginSession()
            login_session.author = user
            login_session.session = session
            login_session.save()
            reply["status"] = 1
            reply["msg"] = ""
            reply["data"] = {'user': get_userdata(user, session)}
        else:
            reply["msg"] = "用户名或密码错误"
    return HttpResponse(json.dumps(reply))


# 检查session是否有效
@csrf_exempt
def app_seesion_valid(request):
    ar = AppRequest(json.loads(request.body))
    reply = ar.reply
    if ar.success:
        reply['data']['user'] = get_userdata(ar.user, ar.session)
    return HttpResponse(json.dumps(ar.reply))

@csrf_exempt
def app_get_categorys(request):
    ar = AppRequest(json.loads(request.body))
    if not ar.success:
        return HttpResponse(json.dumps(ar.reply))
    reply = ar.reply
    categorys = Category.objects.all()
    rdatas = []
    for catagary in categorys:
        cdata = {
            'id': int(catagary.id),
            'name': str(catagary.name)
        }
        rdatas.append(cdata)
    reply['data'] = {"categorys": rdatas}
    return HttpResponse(json.dumps(reply))

@csrf_exempt
def app_get_image_categorys(request):
    ar = AppRequest(json.loads(request.body))
    if not ar.success:
        return HttpResponse(json.dumps(ar.reply))
    reply = ar.reply
    datas = []
    categorys = AppImageCategory.objects.all()
    if len(categorys) == 0:
        get_default_image_category()
        categorys = AppImageCategory.objects.all()
    for category in categorys:
        images = AppUploadImage.objects.filter(category=category)
        image_arr = []
        for image in images:
            image_arr.append({
                'id': image.id,
                'url': image.image.url
            })
        datas.append({
            'category': category.title,
            'category_id': category.id,
            'images': image_arr
            })
    return HttpResponse(get_app_reply(reply, datas))

@csrf_exempt
def image_upload(request):
    ar = AppRequest(request.POST)
    if not ar.success:
        return HttpResponse(json.dumps(ar.reply))
    
    reply = ar.reply
    urls = []
    if request.method == 'POST':
        for key in request.FILES:
            imgextensions = ['jpg', 'png', 'jpeg', 'bmp']
            file = request.FILES[key]
            
            filename = file.name
            fname = u''.join(str(filename))
            isimage = len([i for i in imgextensions if fname.find(i) >= 0]) > 0

            category_id = request.POST.get('category_id')
            categorys = AppImageCategory.objects.filter(id=category_id)

            if len(categorys) == 0:
                category = get_default_image_category()
            else:
                category = categorys.first()

            category_id = category.id

            if not isimage:
                reply["status"] = 0
                reply["msg"] = "仅支持上传图片"
                return HttpResponse(json.dumps(reply))

            url = generate_image_path(None, filename)
            savepath = os.path.normpath(os.path.join(settings.MEDIA_ROOT, url))
            savedir = os.path.dirname(savepath)

            if not os.path.exists(savedir):
                os.makedirs(savedir)

            with open(savepath, 'wb+') as wfile:
                for chunk in file.chunks():
                    wfile.write(chunk)

            from PIL import Image
            image = Image.open(savepath)
            image.save(savepath, quality=20, optimize=True)

            image_url = url
            app_image = AppUploadImage()
            app_image.category = category
            app_image.image.name = image_url
            app_image.save()
            urls.append({
                'url': app_image.image.url,
                'category_id': category_id,
                'image_id': app_image.id
            })

        reply["status"] = 1
        reply["msg"] = "上传成功"
        reply['data'] = {
            'urls': urls
        }

        return HttpResponse(json.dumps(reply))
    else:
        reply["status"] = 0
        reply["msg"] = "only for post"
        return HttpResponse(json.dumps(reply))

@csrf_exempt
def delete_image(request):
    ar = AppRequest(json.loads(request.body))
    if not ar.success:
        return HttpResponse(json.dumps(ar.reply))
    reply = ar.reply
    id = ar.data['image_id']
    images = AppUploadImage.objects.filter(id=id)
    if len(images) == 0:
        reply["status"] = 0
        reply["msg"] = "图片不存在"
    else:
        reply["msg"] = "删除成功"
        reply["data"] = {
            'id': id
        }
        os.remove(os.path.normpath(os.path.join(settings.MEDIA_ROOT, images[0].image.name)))
        images.delete()
    return HttpResponse(json.dumps(reply))

@csrf_exempt
def upload_blog(request):
    ar = AppRequest(json.loads(request.body))
    if not ar.success:
        return HttpResponse(json.dumps(ar.reply))
    reply = ar.reply
    data = ar.data['data']
    categorys = Category.objects.filter(id=data["category"])
    if len(categorys) < 0:
        reply["status"] = 0
        reply["msg"] = "分类不存在"
        reply['data']  = {
            'msg': "分类不存在"
        }
        return HttpResponse(json.dumps(reply))

    exists = Article.objects.filter(title=data['title'])
    if len(exists) > 0:   
        reply["status"] = 0
        reply["msg"] = "文章标题已经存在"
        reply['data']  = {
            'msg': "文章标题已经存在"
        }
        return HttpResponse(json.dumps(reply))

    article = Article()
    article.category = categorys[0]
    article.title = data['title']
    article.body = data['doc']
    article.author = ar.user
    article.save()
    
    reply["status"] = 1
    reply["msg"] = "保存成功"
    reply['data'] = {
        'url': article.get_full_url(),
        'id': article.id,
        'title': article.title
    }
    return HttpResponse(json.dumps(reply))

@csrf_exempt
def app_test(request):
    print(request.POST)
    print(request.FILES)
    return HttpResponse("ss")