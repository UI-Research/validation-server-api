from WebApp.api.v1.models import Run, Budget, Results
from WebApp.api.v1.serializers import RunSerializer, BudgetSerializer, ResultsSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from WebApp.api.v1.permissions import IsOwnerOrNoAccess

class RunList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess]
    serializer_class = RunSerializer

    def get_queryset(self, *args, **kwargs):
        return Run.objects.all().filter(researcher_id=self.request.user).order_by('-run_id')

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

        request.data["total_budget_used"] = total_budget_used

        # TODO: validate

        #instance.total_budget_used = total_budget_used
        #instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        
        return Response(serializer.data)




class ResultList(generics.ListCreateAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    

class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer

