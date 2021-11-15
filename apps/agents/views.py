from django.shortcuts import render
from rest_framework.views import APIView

from Utils.helpers import sendRes
from Utils.auth_utils import VerifyToken, VerifyAdmin
from Utils.pagination import Pagination
from apps.users.serializers import UserSerializer
from .serializers import AgentSerializer
from .models import Agent
import datetime

# Create your views here.
class AgentsView(APIView):
    permission_classes = [ VerifyToken, VerifyAdmin ]
    
    def get(self, request):
        agents = Agent.objects.all()
        paginator = Pagination()
        results = paginator.paginate_queryset(agents, request)
        serialzer = AgentSerializer(results, many=True)
        return paginator.get_paginated_response(serialzer.data)

    def post(self, request):
        random = str(int(datetime.datetime.now().timestamp()))[6:]
        try:
            pwd = random+request.data.get('firstname').lower()
        except:
            return sendRes(400, { "firstname": ["Ce champ est obligatoire"] })
        print(pwd)
        user_serializer = UserSerializer(data={**request.data, 'password': pwd})
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        serializer = AgentSerializer(data={ 'user_id': user_serializer.data.get('id') })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return sendRes(201, msg="Nouvel agent ajouté", data=serializer.data)