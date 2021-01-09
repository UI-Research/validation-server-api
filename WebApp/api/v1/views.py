from WebApp.api.v1.models import Run 
from WebApp.api.v1.serializers import RunSerializer
from rest_framework import generics


class RunList(generics.ListCreateAPIView):
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class RunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
