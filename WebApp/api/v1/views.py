from WebApp.api.v1.models import Run, IntermediateBudget, Budget, Results
from WebApp.api.v1.serializers import RunSerializer, IntermediateBudgetSerializer, BudgetSerializer, ResultsSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from WebApp.api.v1.permissions import IsOwnerOrNoAccess
from WebApp.api.v1.backend import Backend

class RunList(generics.ListCreateAPIView):
    """
    List all runs, create a new run instance
    """
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess]
    serializer_class = RunSerializer

    def get_queryset(self, *args, **kwargs):
        return Run.objects.all().filter(researcher_id=self.request.user).order_by('-run_id')

    def perform_create(self, serializer):
        instance = serializer.save()
        Backend.send_request(instance.run_id)
        return Response(serializer.data)  

class RunDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess]
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class BudgetList(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class BudgetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

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

class IntermediateBudgetList(generics.ListCreateAPIView):
    queryset = IntermediateBudget.objects.all()
    serializer_class = IntermediateBudgetSerializer

class IntermediateBudgetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntermediateBudget.objects.all()
    serializer_class = IntermediateBudgetSerializer

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

class IntermediateBudgetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntermediateBudget.objects.all()
    serializer_class = IntermediateBudgetSerializer

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

class ResultList(generics.ListCreateAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    

class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer


