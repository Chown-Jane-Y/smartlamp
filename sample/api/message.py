# -*- coding: utf-8 -*-


class MessageSuccess(object):

    def __init__(self, data):
        self._data = data

    def data(self):
        message = {
            "code": 0,
            "success": True,
            "data": self._data,
        }
        return message


class MessageError(object):

    def __init__(self, code, message):
        self._code = code
        self._message = message

    def data(self):
        message = {
            "code": self._code,
            "success": False,
            "message": self._message,
        }
        return message
