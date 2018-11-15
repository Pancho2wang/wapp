from django.db import models

# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32, null=True, blank=True)
    user_type = models.IntegerField(default=0)
    enabled = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField(to="Role", null=True, blank=True)
    companys = models.ManyToManyField(to="Company", null=True, blank=True)

class Role(models.Model):
    name = models.CharField(max_length=32)
    alias_name = models.CharField(max_length=32, null=True, blank=True)
    seq = models.IntegerField(default=0, null=True, blank=True)
    is_all_sql_auth = models.IntegerField(default=0)
    enabled = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    resources = models.ManyToManyField(to="Resource", null=True, blank=True)
    sql_resources = models.ManyToManyField(to="SQLResource", null=True, blank=True)
    desc = models.CharField(max_length=512, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Company(models.Model):
    name = models.CharField(max_length=32)
    seq = models.IntegerField(default=0, null=True, blank=True)
    enabled = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    desc = models.CharField(max_length=512, null=True, blank=True)
    roles = models.ManyToManyField(to="Role", null=True, blank=True)

class Resource(models.Model):
    pid = models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=32)
    per_type = models.IntegerField(default=0)
    enabled = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    seq = models.IntegerField(default=0, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    icon = models.CharField(max_length=32, null=True, blank=True)
    desc = models.CharField(max_length=512, null=True, blank=True)
    def __str__(self):
        return self.name

class SQLResource(models.Model):
    name = models.CharField(max_length=32)
    sql_id = models.CharField(max_length=128, unique=True)
    enabled = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    sql_script = models.CharField(max_length=2048, null=True, blank=True)
    seq = models.IntegerField(default=0, null=True, blank=True)
    desc = models.CharField(max_length=512, null=True, blank=True)
    def __str__(self):
        return self.name

class LoginStatus(models.Model):
    user = models.ForeignKey(to="User",on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    status = models.IntegerField(default=1)
    active_time = models.IntegerField(default=30)
    update_time = models.DateTimeField(auto_now=True)

class OperateLog(models.Model):
    name = models.CharField(max_length=128)
    action_type = models.CharField(max_length=64)
    action_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=64)
    user_id = models.IntegerField(null=True, blank=True)
    param = models.CharField(max_length=512, null=True, blank=True)
    result = models.CharField(max_length=512, null=True, blank=True)