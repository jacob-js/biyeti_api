from rest_framework.response import Response

def sendRes(status, error=None, msg=None, data=None):
    return Response({ 'error': error, 'msg': msg, 'data': data }, status=status)