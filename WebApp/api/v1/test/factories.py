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


#class UserFactory(factory.django.DjangoModelFactory):
#    class Meta:
#        model = User #'users.User'  # Equivalent to ``model = myapp.models.User``

#    username = factory.Sequence(lambda n: 'john%s' % n)
#    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
#    date_joined = factory.LazyFunction(datetime.datetime.now)

#class ResearcherUserFactory(UserFactory):
#    groups.add(Group.objects.get(name='Researcher'))


class RunFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Run
  
    researcher_id = factory.SubFactory(UserFactory)
    run_type = 1
    sanitized_run_input = factory.Dict( {'run':['test'],}, dict_factory=JSONFactory)


class BudgetFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Budget

