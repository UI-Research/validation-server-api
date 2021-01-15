from django.urls import path
from WebApp.api.v1 import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('runs/', views.RunList.as_view()),
    path('runs/<int:pk>/', views.RunDetail.as_view()),
    path('budget/', views.BudgetList.as_view()),
    path('budget/<int:pk>', views.BudgetDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
