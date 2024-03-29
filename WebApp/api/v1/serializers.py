from rest_framework import serializers
from WebApp.api.v1.models import Command, SyntheticDataRun, SyntheticDataResult
from WebApp.api.v1.models import ConfidentialDataRun, ConfidentialDataResult
from WebApp.api.v1.models import ReviewAndRefinementBudget, PublicUseBudget

class CommandSerializer(serializers.ModelSerializer):
    researcher_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Command
        fields = '__all__'


class SyntheticDataRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticDataRun
        fields = [
            "command_id",
            "run_id",
            "researcher_id",
            "epsilon", 
            "date_time_run_submitted"
            ]

class SyntheticDataResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticDataResult
        fields = [
            "command_id",
            "run_id",
            "researcher_id",
            "accuracy",
            "result",
            "privacy_budget_used"
        ]

class ConfidentialDataRunSerializer(serializers.ModelSerializer):
    researcher_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ConfidentialDataRun
        fields = [
            "command_id",
            "run_id",
            "researcher_id",
            "epsilon", 
            "date_time_run_submitted"
            ]


class ConfidentialDataResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfidentialDataResult
        fields = [
            "command_id",
            "run_id",
            "researcher_id",
            "accuracy",
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_budget_available'] = instance.total_budget_allocated - instance.total_budget_used
        return representation

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_budget_available'] = instance.total_budget_allocated - instance.total_budget_used
        return representation

    class Meta:
        model = PublicUseBudget
        fields = [
            "researcher_id",
            "total_budget_allocated",
            "total_budget_used"
        ]

