from django.urls import path
from WebApp.api.v1 import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('command/', views.CommandList.as_view(), name='command-list'),
    path('command/<int:pk>/', views.CommandDetail.as_view(), name='command-detail'),
    path('review-and-refinement-budget/', views.ReviewAndRefinementBudgetList.as_view(), name='review-and-refinement-budget-list'),
    path('review-and-refinement-budget/<int:pk>/', views.ReviewAndRefinementBudgetDetail.as_view(), name='review-and-refinement-budget-detail'),
    path('public-use-budget/', views.PublicUseBudgetList.as_view(), name='public-use-budget-list'),
    path('public-use-budget/<int:pk>/', views.PublicUseBudgetDetail.as_view(), name='public-use-budget-detail'),
    path('confidential-data-result/', views.ConfidentialDataResultList.as_view(), name='confidential-data-result-list'),
    path('confidential-data-result/<int:pk>/', views.ConfidentialDataResultDetail.as_view(), name='confidential-data-result-detail'),
    path('confidential-data-run/', views.ConfidentialDataRunList.as_view(), name='confidential-data-result-list'),
    path('confidential-data-run/<int:pk>/', views.ConfidentialDataRunDetail.as_view(), name='confidential-data-result-detail'),
    path('synthetic-data-result/', views.SyntheticDataResultList.as_view(), name='synthetic-data-result-list'),
    path('synthetic-data-result/<int:pk>/', views.SyntheticDataResultDetail.as_view(), name='synthetic-data-result-detail'),
    path('synthetic-data-run/', views.SyntheticDataRunList.as_view(), name='synthetic-data-result-list'),
    path('synthetic-data-run/<int:pk>/', views.SyntheticDataRunDetail.as_view(), name='synthetic-data-result-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
