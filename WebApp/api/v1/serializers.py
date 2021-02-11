from rest_framework import serializers
from WebApp.api.v1.models import Run, Budget, Results

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = [
            'run_id', 'researcher_id', 'run_type', 'sanitized_run_input', 
            'display_results_decision', 'display_results_number',
            'date_time_run_submitted'
            ]

            
class BudgetSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data["total_budget_used"] > data["total_budget_allocated"]:
            raise serializers.ValidationError("Cannot exceed budget allocation")

        return data

    class Meta:
        model = Budget
        fields = [
            "researcher_id",
            "total_budget_allocated",
            "total_budget_used"
        ]

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = [
            "result_id",
            "run_id",
            "researcher_id",
            "result",
            "return_to_researcher",
            "budget_used"
        ]
