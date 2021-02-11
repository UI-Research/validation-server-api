from django.urls import path
from WebApp.api.v1 import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('runs/', views.RunList.as_view(), name='run-list'),
    path('runs/<int:pk>/', views.RunDetail.as_view()),
    path('budget/', views.BudgetList.as_view()),
    path('budget/<uuid:pk>/', views.BudgetDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
