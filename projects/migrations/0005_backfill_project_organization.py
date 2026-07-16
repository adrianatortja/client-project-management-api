from django.db import migrations
from django.utils.text import slugify


def backfill_organizations(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Organization = apps.get_model('orgs', 'Organization')
    Membership = apps.get_model('orgs', 'Membership')
    Plan = apps.get_model('billing', 'Plan')
    Subscription = apps.get_model('billing', 'Subscription')

    free_plan = Plan.objects.filter(name='free').first()
    org_by_user_id = {}

    for project in Project.objects.filter(organization__isnull=True).select_related('created_by'):
        user = project.created_by

        if user.id not in org_by_user_id:
            existing_membership = Membership.objects.filter(user=user, role='owner').first()

            if existing_membership:
                org = existing_membership.organization
            else:
                base_slug = slugify(user.username) or f'org-{user.id}'
                slug = base_slug
                suffix = 1
                while Organization.objects.filter(slug=slug).exists():
                    suffix += 1
                    slug = f'{base_slug}-{suffix}'
                org = Organization.objects.create(
                    name=f"{user.username}'s Organization", slug=slug
                )
                Membership.objects.create(organization=org, user=user, role='owner')

            if free_plan and not Subscription.objects.filter(organization=org).exists():
                Subscription.objects.create(organization=org, plan=free_plan)

            org_by_user_id[user.id] = org

        project.organization = org_by_user_id[user.id]
        project.save(update_fields=['organization'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_organization_created_by'),
        ('billing', '0002_seed_plans'),
    ]

    operations = [
        migrations.RunPython(backfill_organizations, noop),
    ]
