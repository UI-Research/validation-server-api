from WebApp.api.v1.models import Run, Budget
from WebApp.api.v1.serializers import RunSerializer, BudgetSerializer
from rest_framework import generics


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