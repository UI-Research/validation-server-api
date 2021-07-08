from WebApp.api.v1.models import Command, SyntheticDataRun, SyntheticDataResult
from WebApp.api.v1.models import ConfidentialDataRun, ConfidentialDataResult
from WebApp.api.v1.models import ReviewAndRefinementBudget, PublicUseBudget
from WebApp.api.v1.serializers import CommandSerializer, SyntheticDataRunSerializer, ConfidentialDataRunSerializer
from WebApp.api.v1.serializers import ReviewAndRefinementBudgetSerializer, PublicUseBudgetSerializer
from WebApp.api.v1.serializers import SyntheticDataResultSerializer, ConfidentialDataResultSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from WebApp.api.v1.permissions import IsOwnerOrNoAccess
from WebApp.api.v1.backend import Backend

class CommandList(generics.ListCreateAPIView):
    """
    List all runs, create a new run instance
    """
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess]
    serializer_class = CommandSerializer

    def get_queryset(self, *args, **kwargs):
        return Command.objects.all().filter(researcher_id=self.request.user).order_by('-command_id')

    def perform_create(self, serializer):
        instance = serializer.save()
        Backend.send_request(instance.run_id)
        return Response(serializer.data)  

class CommandDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess]
    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class ReviewAndRefinementBudgetList(generics.ListCreateAPIView):
    queryset = ReviewAndRefinementBudget.objects.all()
    serializer_class = ReviewAndRefinementBudgetSerializer

class ReviewAndRefinementBudgetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReviewAndRefinementBudget.objects.all()
    serializer_class = ReviewAndRefinementBudgetSerializer

    def update(self, request, *args, **kwargs):
        # http://www.cdrf.co/3.1/rest_framework.generics/RetrieveUpdateDestroyAPIView.html
        instance = self.get_object()
        
        total_budget_used = instance.total_budget_used
        total_budget_allocated = instance.total_budget_allocated

        budget_used = float(request.data.get("budget_used"))
        total_budget_used = float(total_budget_used) + budget_used

        data = request.data.copy()
        data["total_budget_used"] = total_budget_used
        
        # TODO: validate

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class PublicUseBudgetList(generics.ListCreateAPIView):
    queryset = PublicUseBudget.objects.all()
    serializer_class = PublicUseBudgetSerializer

class PublicUseBudgetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PublicUseBudget.objects.all()
    serializer_class = PublicUseBudgetSerializer

    def update(self, request, *args, **kwargs):
        # http://www.cdrf.co/3.1/rest_framework.generics/RetrieveUpdateDestroyAPIView.html
        instance = self.get_object()
        
        total_budget_used = instance.total_budget_used
        total_budget_allocated = instance.total_budget_allocated

        budget_used = float(request.data.get("budget_used"))
        total_budget_used = float(total_budget_used) + budget_used

        data = request.data.copy()
        data["total_budget_used"] = total_budget_used
        
        # TODO: validate

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class ConfidentialDataResultList(generics.ListCreateAPIView):
    queryset = ConfidentialDataResult.objects.all()
    serializer_class = ConfidentialDataResultSerializer
    

class ConfidentialDataResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfidentialDataResult.objects.all()
    serializer_class = ConfidentialDataResultSerializer

class ConfidentialDataRunList(generics.ListCreateAPIView):
    queryset = ConfidentialDataRun.objects.all()
    serializer_class = ConfidentialDataRunSerializer
    

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
    queryset = SyntheticDataRun.objects.all()
    serializer_class = SyntheticDataRunSerializer
    

class SyntheticDataRunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SyntheticDataRun.objects.all()
    serializer_class = SyntheticDataRunSerializer
