class Message(object):
    def __init__(self):
        self.code = 200
        self.msg = None
        self.data = None
    
    @staticmethod
    def success(code = 200, data = None, msg = None):
        return Message.message(code, data, msg)
    
    @staticmethod
    def error(code = 400, msg = None):
        return Message.message(code, msg)

    @staticmethod
    def message(code = 0, data = None, msg = None):
        return {'code': code, 'data': data, 'msg': msg}