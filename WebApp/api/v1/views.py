from WebApp.api.v1.models import Run, Budget, Results
from WebApp.api.v1.serializers import RunSerializer, BudgetSerializer, ResultsSerializer
from rest_framework import generics
from rest_framework.response import Response

class RunList(generics.ListCreateAPIView):
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class RunDetail(generics.RetrieveUpdateDestroyAPIView):
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




class ResultsList(generics.ListCreateAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer

class ResultsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer