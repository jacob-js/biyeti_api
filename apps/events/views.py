from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from Utils.helpers import sendRes

from Utils.pagination import Pagination

from .serializers import EventSerializer
from .models import Event, Category

# Create your views here.
@api_view(['GET', 'POST'])
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
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=201, data=serializer.data, msg="Evénement enregistré")
        return sendRes(status=400, error=serializer.errors)