from django.shortcuts import render
from rest_framework.views import APIView

from Utils.helpers import sendRes
from Utils.auth_utils import VerifyToken, VerifyAdmin
from Utils.pagination import Pagination
from .serializers import AgentSerializer
from .models import Agent

# Create your views here.
class AgentsView(APIView):
    permission_classes = [ VerifyToken, VerifyAdmin ]
    
    def get(self, request):
        agents = Agent.objects.all()
        paginator = Pagination()
        results = paginator.paginate_queryset(agents, request)
        serialzer = AgentSerializer(results, many=True)
        return paginator.get_paginated_response(serialzer.data)

    # def post(self, request):
    #     page