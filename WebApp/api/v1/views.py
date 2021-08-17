from WebApp.api.v1.models import Command, SyntheticDataRun, SyntheticDataResult
from WebApp.api.v1.models import ConfidentialDataRun, ConfidentialDataResult
from WebApp.api.v1.models import ReviewAndRefinementBudget, PublicUseBudget
from WebApp.api.v1.serializers import CommandSerializer, SyntheticDataRunSerializer, ConfidentialDataRunSerializer
from WebApp.api.v1.serializers import ReviewAndRefinementBudgetSerializer, PublicUseBudgetSerializer
from WebApp.api.v1.serializers import SyntheticDataResultSerializer, ConfidentialDataResultSerializer
from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from WebApp.api.v1.permissions import IsAdministrator, IsOwner
from WebApp.api.v1.backend import Backend

import boto3
import json

class CommandList(generics.ListCreateAPIView):
    """
    List all commands, create a new command instance
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CommandSerializer

    def get_queryset(self, *args, **kwargs):
        return Command.objects.all().filter(researcher_id=self.request.user).order_by('-command_id')

    def perform_create(self, serializer):
        serializer.save(researcher_id=self.request.user)

class CommandDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

class ReviewAndRefinementBudgetList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = ReviewAndRefinementBudgetSerializer

    def get_queryset(self, *args, **kwargs):
        return ReviewAndRefinementBudget.objects.all().filter(researcher_id=self.request.user)

class ReviewAndRefinementBudgetDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdministrator]
    serializer_class = ReviewAndRefinementBudgetSerializer
    queryset = ReviewAndRefinementBudget.objects.all()

    def update(self, request, *args, **kwargs):
        # http://www.cdrf.co/3.1/rest_framework.generics/RetrieveUpdateDestroyAPIView.html
        instance = self.get_object()
        
        total_budget_used = instance.total_budget_used

        budget_used = float(request.data.get("privacy_budget_used"))
        total_budget_used = float(total_budget_used) + budget_used

        data = request.data.copy()
        data["total_budget_used"] = total_budget_used
        data["total_budget_allocated"] = instance.total_budget_allocated
        
        # TODO: validate

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class PublicUseBudgetList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PublicUseBudgetSerializer

    def get_queryset(self, *args, **kwargs):
        return PublicUseBudget.objects.all().filter(researcher_id=self.request.user)

class PublicUseBudgetDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdministrator]
    serializer_class = PublicUseBudgetSerializer
    queryset = ReviewAndRefinementBudget.objects.all()

    def update(self, request, *args, **kwargs):
        # http://www.cdrf.co/3.1/rest_framework.generics/RetrieveUpdateDestroyAPIView.html
        instance = self.get_object()
        
        total_budget_used = instance.total_budget_used

        budget_used = float(request.data.get("privacy_budget_used"))
        total_budget_used = float(total_budget_used) + budget_used

        data = request.data.copy()
        data["total_budget_used"] = total_budget_used
        data["total_budget_allocated"] = instance.total_budget_allocated
        
        # TODO: validate

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class PublicUseBudgetRetrieve(mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = PublicUseBudget.objects.all()
    serializer_class = PublicUseBudgetSerializer


class ConfidentialDataResultList(generics.ListCreateAPIView):
    queryset = ConfidentialDataResult.objects.all()
    serializer_class = ConfidentialDataResultSerializer
    

class ConfidentialDataResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfidentialDataResult.objects.all()
    serializer_class = ConfidentialDataResultSerializer

class ConfidentialDataRunList(generics.ListCreateAPIView):
    serializer_class = ConfidentialDataRunSerializer

    def get_queryset(self):
        queryset = ConfidentialDataRun.objects.all()
        command = self.request.query_params.get('command_id')

        if command is not None:
            queryset = queryset.filter(command_id=command)

        return queryset

    

class ConfidentialDataRunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfidentialDataRun.objects.all()
    serializer_class = ConfidentialDataRunSerializer

class SyntheticDataResultList(generics.ListCreateAPIView):
    queryset = SyntheticDataResult.objects.all()
    serializer_class = SyntheticDataResultSerializer
    

class SyntheticDataResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SyntheticDataResult.objects.all()
    serializer_class = SyntheticDataResultSerializer

class SyntheticDataRunList(generics.ListCreateAPIView):
    serializer_class = SyntheticDataRunSerializer

    # Show all of the runs of a particular command
    def get_queryset(self):
        queryset = SyntheticDataRun.objects.all()
        command = self.request.query_params.get('command_id')

        if command is not None:
            queryset = queryset.filter(command_id=command)

        return queryset



class SyntheticDataRunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SyntheticDataRun.objects.all()
    serializer_class = SyntheticDataRunSerializer
