from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from Utils.auth_utils import CanUserChangeEntrys
from Utils.helpers import sendRes

from Utils.pagination import Pagination

from .serializers import EventSerializer
from .models import Event, Category

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([CanUserChangeEntrys])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def events_view(request):
    if request.method == 'GET':
        category_id = request.query_params.get('category_id')
        events = []
        if category_id:
            events = Event.objects.filter(category_id=category_id).order_by('-event_date')
        else:
            events = Event.objects.all().order_by('-event_date')
        paginator = Pagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data={**request.data.copy(), 'user': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=201, data=serializer.data, msg="Evénement enregistré")
        return sendRes(status=400, error=serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanUserChangeEntrys])
def event_view(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return sendRes(status=404, error="Evénement introuvable")

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return sendRes(status=200, data=serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=200, data=serializer.data, msg="Evénement modifié")
        return sendRes(status=400, error=serializer.errors)

    elif request.method == 'DELETE':
        event.delete()
        return sendRes(status=204, msg="Evénement supprimé")