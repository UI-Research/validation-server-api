from django.db import models
from django.conf import settings

class Run(models.Model):
    RUN_TYPE_CHOICES = [
        (1, 'OLS'),
        (2, 'Tabulation'),
    ]

    run_id = models.AutoField(primary_key=True)
    researcher_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run_type = models.IntegerField(choices=RUN_TYPE_CHOICES)
    sanitized_run_input = models.JSONField()
    display_results_decision = models.BooleanField(default=False)
    display_results_number = models.IntegerField(default=1)
    date_time_run_submitted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Run_{self.run_id}"

class Budget(models.Model):
    researcher_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    total_budget_allocated = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=100)
    total_budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

class Results(models.Model):
    result_id = models.AutoField(primary_key=True)
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    researcher_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = models.JSONField()
    return_to_researcher = models.BooleanField(default=False)
    budget_used = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0)

