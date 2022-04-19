from django.shortcuts import render
from rest_framework.views import APIView

from Utils.helpers import sendRes
from Utils.auth_utils import VerifyToken, VerifyAdmin
from Utils.pagination import Pagination
from apps.users.serializers import UserSerializer
from .serializers import AgentSerializer
from .models import Agent
import datetime
from random import randint

# Create your views here.
class AgentsView(APIView):
    permission_classes = [ VerifyToken ]
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        event_id = request.query_params.get('event_id')
        agents = []
        if user_id:
            agents = Agent.objects.filter(user=user_id)
        elif event_id:
            agents = Agent.objects.filter(event=event_id)
        else:
            agents = Agent.objects.all().order_by('-id')
        paginator = Pagination()
        results = paginator.paginate_queryset(agents, request)
        serialzer = AgentSerializer(results, many=True)
        return paginator.get_paginated_response(serialzer.data)

    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return sendRes(201, msg="Nouvel agent ajouté", data=serializer.data)

class AgentDetailView(APIView):
    permission_classes = [VerifyToken, VerifyAdmin]

    def get(self, request, id):
        try:
            agent = Agent.objects.get(id=id)
        except Agent.DoesNotExist:
            return sendRes(404, "Agent introuvable")
        serialzer = AgentSerializer(agent)
        return sendRes(200, data=serialzer.data)

    def put(self, request, id):
        try:
            agent = Agent.objects.get(id=id)
            AgentSerializer.update(agent, **request.data)
        except Agent.DoesNotExist:
            return sendRes(404, "Agent introuvable")

    def delete(self, request, id):
        try:
            agent = Agent.objects.get(id=id)
        except Agent.DoesNotExist:
            return sendRes(404, "Agent introuvable")
        agent.delete()
        return sendRes(200, msg="Agent supprimé")