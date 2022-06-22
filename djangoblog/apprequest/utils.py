
from email.policy import default
from .models import *
from accounts.models import BlogUser
import json

def get_userdata(user, session):
    return {
                'nickname': str(user.nickname),
                'username': str(user.username),
                'session': session
            }

class AppRequest:

    FormData = 0
    JsonData = 1

    def __init__(self, verify_data) -> None:
        self.data = verify_data
        username = self.data.get('username', None)
        self.session = self.data.get('session', None)
        self.success = False
        self.reply =  {"status": 0, "msg": "验证失败", "data": {"valid": 0}}
        try:
            self.user = BlogUser.objects.get(username=username)
            login_session = AppLoginSession.objects.get(author=self.user)
            if login_session and login_session.session == self.session:
                self.success = True
                self.reply['status'] = 1
                self.reply['msg'] = ''
                self.reply['data'] = {
                    'valid:': 1
                }
        except:
            pass

def get_app_reply(reply, data=None):
    if data:
        reply['data'] = {'data': data}
    return json.dumps(reply)