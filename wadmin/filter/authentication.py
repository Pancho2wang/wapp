from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException
import datetime
from wadmin.models import *

class WAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        if not token:
            raise APIException('验证失败')
            return
        obj=LoginStatus.objects.filter(token=token,status=1).first()
        if not obj:
            raise APIException('没有通过验证')
            return
        now = datetime.datetime.now()
        enabled_time = obj.update_time + datetime.timedelta(minutes=obj.active_time)
        if now > enabled_time:
            raise APIException('验证已失效')
            return
        user = User.objects.filter(id=obj.user_id,enabled=1,status=1).first()
        if not user:
            raise APIException('用户已失效')
            return
        obj.save()
        return (obj.token, user)
        
        