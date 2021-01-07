from django.db import models
from django.conf import settings

class Run(models.Model):
    RUN_TYPE_CHOICES = [
        (1, 'OLS'),
        (2, 'Tabulation'),
    ]

    run_id = models.IntegerField(primary_key=True, unique=True)
    researcher_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run_type = models.IntegerField(choices=RUN_TYPE_CHOICES)
    sanitized_run_input = models.JSONField()
    display_results_decision = models.BooleanField(default=False)
    display_results_number = models.IntegerField(default=1)
    date_time_run_submitted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.run_id;

