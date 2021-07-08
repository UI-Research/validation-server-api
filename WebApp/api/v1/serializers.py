from rest_framework import serializers
from WebApp.api.v1.models import Command, SyntheticDataRun, SyntheticDataResult
from WebApp.api.v1.models import ConfidentialDataRun, ConfidentialDataResult
from WebApp.api.v1.models import ReviewAndRefinementBudget, PublicUseBudget

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = [
            "researcher_id", 
            "command_id",
            "command_type", 
            "sanitized_command_input"
            ]

class SyntheticDataRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = [
            "command_id",
            "run_id",
            "epsilon", 
            "date_time_run_submitted"
            ]

class SyntheticDataResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticDataResult
        fields = [
            "command_id",
            "run_id",
            "result",
            "privacy_budget_used"
        ]


class ConfidentialDataRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = [
            "command_id",
            "run_id",
            "epsilon", 
            "date_time_run_submitted"
            ]

class ConfidentialDataResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfidentialDataResult
        fields = [
            "command_id",
            "run_id",
            "result",
            "display_results_decision",
            "release_results_decision",
            "privacy_budget_used"
        ]

            
class ReviewAndRefinementBudgetSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data["total_budget_used"] > data["total_budget_allocated"]:
            raise serializers.ValidationError("Cannot exceed budget allocation")

        return data

    class Meta:
        model = ReviewAndRefinementBudget
        fields = [
            "researcher_id",
            "total_budget_allocated",
            "total_budget_used"
        ]

class PublicUseBudgetSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data["total_budget_used"] > data["total_budget_allocated"]:
            raise serializers.ValidationError("Cannot exceed budget allocation")

        return data

    class Meta:
        model = PublicUseBudget
        fields = [
            "researcher_id",
            "total_budget_allocated",
            "total_budget_used"
        ]

