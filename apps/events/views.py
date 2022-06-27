from datetime import datetime
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from Utils.auth_utils import CanUserChangeEntrys, CheckIsAgentEditingData, CheckIsEventAdminEditingData, IsAdminEditingData
from Utils.helpers import sendRes
from Utils.pagination import Pagination

from .serializers import CategorySerializer, EventSerializer
from .models import Event, Category

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([CanUserChangeEntrys])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def events_view(request):
    """
    List all events, or create a new event.
    """
    if request.method == 'GET':
        category_id = request.query_params.get('category_id')
        coming = request.query_params.get('coming')
        order_by = request.query_params.get('order_by', '-event_date')
        events = []
        if bool(coming):
            events = Event.objects.filter(event_date__gte=datetime.now()).order_by(order_by)
        if category_id:
            events = Event.objects.filter(category_id=category_id).order_by(order_by)
        else:
            events = Event.objects.all().order_by(order_by)
        paginator = Pagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        serializer = EventSerializer(data={**request.data.copy(), 'user': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=201, data=serializer.data, msg="Evénement enregistré")
        return sendRes(status=400, error=serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanUserChangeEntrys, CheckIsAgentEditingData, CheckIsEventAdminEditingData])
def event_view(request, event_id):
    """
    Retrieve, update or delete a event instance.
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return sendRes(status=404, error="Evénement introuvable")

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return sendRes(status=200, data=serializer.data)

    if request.method == 'PUT':
        serializer = EventSerializer(event, data={**request.data, 'user': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=200, data=serializer.data, msg="Evénement modifié")
        return sendRes(status=400, error=serializer.errors)

    if request.method == 'DELETE':
        event.delete()
        return sendRes(status=204, msg="Evénement supprimé")

@api_view(['GET', 'POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
@permission_classes([CanUserChangeEntrys, IsAdminEditingData])
def categorys_view(request):
    """
    List all categories, or create a new category.
    """
    if(request.method == 'GET'):
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)
        return sendRes(status=200, data=serializer.data)

    if(request.method == 'POST'):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return sendRes(status=201, data=serializer.data, msg="Catégorie enregistrée")
        return sendRes(status=400, error=serializer.errors)

@api_view(['GET'])
def search_events_view(request):
    """
    Search events.
    """
    query = request.query_params.get('query')
    if query:
        search_vector = SearchVector('name', 'description', 'category__name', 'location')
        search_query = SearchQuery(query)
        events = Event.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')
        paginator = Pagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    return sendRes(status=400, error="Requête invalide")
    