from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Company)
admin.site.register(Resource)
admin.site.register(SQLResource)
admin.site.register(LoginStatus)
admin.site.register(OperateLog)