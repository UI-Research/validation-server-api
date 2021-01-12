from rest_framework import serializers
from WebApp.api.v1.models import Run, Budget

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = [
            'run_id', 'researcher_id', 'run_type', 'sanitized_run_input', 
            'display_results_decision', 'display_results_number',
            'date_time_run_submitted'
            ]

            
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            "researcher_id",
            "budget_allocated",
            "budget_used"
        ]
