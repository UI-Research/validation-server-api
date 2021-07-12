from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from WebApp.users.models import User


class Command(models.Model):
    COMMAND_TYPE_CHOICES = [
        (1, 'OLS'),
        (2, 'Tabulation'),
    ]

    researcher_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    command_id = models.AutoField(primary_key=True)
    command_type = models.IntegerField(choices=COMMAND_TYPE_CHOICES)
    sanitized_command_input = models.JSONField()

    def __str__(self):
        return f"Run_{self.command_id}"

class SyntheticDataRun(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)
    run_id = models.AutoField(primary_key=True)
    epsilon = models.DecimalField(decimal_places=2, max_digits=5)
    date_time_run_submitted = models.DateTimeField(auto_now_add=True)

class SyntheticDataResult(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)
    run_id = models.AutoField(primary_key=True)
    result = models.JSONField()
    privacy_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

class ConfidentialDataRun(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)
    run_id = models.AutoField(primary_key=True)
    epsilon = models.DecimalField(decimal_places=2, max_digits=5)
    date_time_run_submitted = models.DateTimeField(auto_now_add=True)

class ConfidentialDataResult(models.Model):
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)
    run_id = models.AutoField(primary_key=True)
    result = models.JSONField()
    display_results_decision = models.BooleanField(default=False)
    release_results_decision = models.BooleanField(default=False)
    privacy_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

class ReviewAndRefinementBudget(models.Model):
    researcher_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    total_budget_allocated = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=100)
    total_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

@receiver(post_save, sender=User)
def create_review_and_refinement_budget(sender, instance, created, **kwargs):
    if created:
        ReviewAndRefinementBudget.objects.create(researcher_id=instance)

class PublicUseBudget(models.Model):
    researcher_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    total_budget_allocated = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=100)
    total_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

@receiver(post_save, sender=User)
def create_public_use_budget(sender, instance, created, **kwargs):
    if created:
        PublicUseBudget.objects.create(researcher_id=instance)

