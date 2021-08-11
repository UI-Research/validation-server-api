from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from WebApp.users.models import User
from WebApp.api.v1.utilities import trigger_smartnoise

import boto3
import json
import os

class Command(models.Model):
    COMMAND_TYPE_CHOICES = [
        (1, 'OLS'),
        (2, 'Tabulation'),
    ]

    command_id = models.AutoField(primary_key=True)
    command_name = models.CharField(max_length=100, default="Command_title")
    command_type = models.IntegerField(choices=COMMAND_TYPE_CHOICES)
    researcher_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commands', on_delete=models.CASCADE, db_column="researcher_id")
    sanitized_command_input = models.JSONField()
    
    class Meta:
        unique_together = [["command_name", "researcher_id"]]

class SyntheticDataRun(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE, db_column='command_id')
    run_id = models.AutoField(primary_key=True)
    epsilon = models.DecimalField(decimal_places=2, max_digits=5)
    date_time_run_submitted = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Command)
def create_synthetic_data_run(sender, instance, created, **kwargs):
    if created:
        SyntheticDataRun.objects.create(command_id=instance, epsilon=1.0)

@receiver(post_save, sender=SyntheticDataRun)
def trigger_synthetic_data_run(sender, instance, created, **kwargs):
    if created:
        trigger_smartnoise(instance, confidential_query=False)

class SyntheticDataResult(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE, db_column='command_id')
    run_id = models.OneToOneField(SyntheticDataRun, primary_key = True, on_delete=models.CASCADE, db_column='run_id')
    accuracy = models.JSONField()
    result = models.JSONField()
    privacy_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

class ConfidentialDataRun(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE, db_column='command_id')
    run_id = models.AutoField(primary_key=True)
    epsilon = models.DecimalField(decimal_places=2, max_digits=5)
    date_time_run_submitted = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=ConfidentialDataRun)
def trigger_synthetic_data_run(sender, instance, created, **kwargs):
    if created:
        trigger_smartnoise(instance, confidential_query=True)

class ConfidentialDataResult(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE, db_column='command_id')
    run_id = models.OneToOneField(ConfidentialDataRun, primary_key=True, on_delete=models.CASCADE, db_column='run_id')
    accuracy = models.JSONField()
    result = models.JSONField()
    display_results_decision = models.BooleanField(default=False)
    release_results_decision = models.BooleanField(default=False)
    privacy_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

class ReviewAndRefinementBudget(models.Model):
    researcher_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, db_column='researcher_id')
    total_budget_allocated = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=100)
    total_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

@receiver(post_save, sender=User)
def create_review_and_refinement_budget(sender, instance, created, **kwargs):
    if created:
        ReviewAndRefinementBudget.objects.create(researcher_id=instance)

class PublicUseBudget(models.Model):
    researcher_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, db_column='researcher_id')
    total_budget_allocated = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=100)
    total_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

@receiver(post_save, sender=User)
def create_public_use_budget(sender, instance, created, **kwargs):
    if created:
        PublicUseBudget.objects.create(researcher_id=instance)
