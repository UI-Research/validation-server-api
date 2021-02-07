import factory
from ..models import Run, Budget
from WebApp.users.test.factories import UserFactory
import json


class JSONFactory(factory.DictFactory):
    """
    Use with factory.Dict to make JSON strings.
    """
    @classmethod
    def _generate(cls, create, attrs):
        obj = super()._generate(create, attrs)


class RunFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Run
  
    researcher_id = factory.SubFactory(UserFactory)
    run_type = 1
    sanitized_run_input = factory.Dict( {'run':['test'],}, dict_factory=JSONFactory)


class BudgetFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Budget

