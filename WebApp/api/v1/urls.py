from django.urls import path
from WebApp.api.v1 import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('runs/', views.RunList.as_view(), name='run-list'),
    path('runs/<int:pk>/', views.RunDetail.as_view(), name='run-detail'),
    path('budget/', views.BudgetList.as_view(), name='budget-list'),
    path('budget/<int:pk>/', views.BudgetDetail.as_view(), name='budget-detail'),
    path('intermediate-budget/', views.IntermediateBudgetList.as_view(), name='intermediate-budget-list'),
    path('intermediate-budget/<int:pk>/', views.IntermediateBudgetDetail.as_view(), name='intermediate-budget-detail'),
    path('result/', views.ResultList.as_view(), name='result-list'),
    path('result/<int:pk>/', views.ResultDetail.as_view(), name='result-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
