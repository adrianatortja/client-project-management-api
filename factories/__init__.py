import factory
from django.contrib.auth import get_user_model

from billing.models import Plan, Subscription
from orgs.models import Membership, Organization
from projects.models import Project, Task

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop('password', 'testpass123')
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, password=password, **kwargs)


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f'Org {n}')
    slug = factory.Sequence(lambda n: f'org-{n}')


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    organization = factory.SubFactory(OrganizationFactory)
    user = factory.SubFactory(UserFactory)
    role = Membership.ROLE_MEMBER


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan
        django_get_or_create = ('name',)

    name = Plan.FREE
    max_projects = 3


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    organization = factory.SubFactory(OrganizationFactory)
    plan = factory.SubFactory(PlanFactory)


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    organization = factory.SubFactory(OrganizationFactory)
    created_by = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'Project {n}')
    status = 'active'


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    project = factory.SubFactory(ProjectFactory)
    title = factory.Sequence(lambda n: f'Task {n}')
    completed = False
