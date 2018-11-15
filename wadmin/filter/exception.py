from rest_framework.views import exception_handler
from wadmin.utils.message import Message

def w_exception_handler(exc,context):
    response = exception_handler(exc, context) #获取本来应该返回的exception的response 
    if response is not None:
      response.data = Message.error(401, response.data['detail'])
      # del response.data['detail']  #删掉原来的detail
    return response