from django.contrib import admin
from .models import Command, ReviewAndRefinementBudget, PublicUseBudget
from .models import SyntheticDataResult, ConfidentialDataResult
from .models import SyntheticDataRun, ConfidentialDataRun

admin.site.register(SyntheticDataRun)
admin.site.register(ConfidentialDataRun)
