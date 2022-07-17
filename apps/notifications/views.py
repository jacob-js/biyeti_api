from rest_framework.decorators import api_view, permission_classes

from Utils.auth_utils import VerifyToken
from Utils.helpers import sendRes
from Utils.pagination import Pagination
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

@api_view(['GET'])
@permission_classes([VerifyToken])
def get_user_notifications(request):
    """
    This function is used to get user's notifications
    """
    notifications = Notification.objects.filter(user_receiver__id=request.user.id)
    if "status" in request.query_params:
        notifications = notifications.filter(user_receiver__id=request.user.id, status=request.query_params["status"])
    paginator = Pagination()
    results = paginator.paginate_queryset(notifications, request)
    serializer = NotificationSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([VerifyToken])
def notification_detail(request, notif_id):
    """
    This function is used to get or update a notification
    """
    try:
        notification = Notification.objects.get(id=notif_id)
    except Notification.DoesNotExist:
        return sendRes(404, message="Notification not found")
    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return sendRes(200, data=serializer.data)
    if request.method == 'PUT':
        notification.status = "read"
        notification.save()
        return sendRes(200, data=serializer.data)
    return sendRes(400, message="Method not allowed")
