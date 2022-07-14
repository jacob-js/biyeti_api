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
    paginator = Pagination()
    results = paginator.paginate_queryset(notifications, request)
    serializer = NotificationSerializer(results, many=True)
    return sendRes(200, data=serializer.data)
