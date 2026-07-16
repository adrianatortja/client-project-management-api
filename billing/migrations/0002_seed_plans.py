from django.db import migrations


def seed_plans(apps, schema_editor):
    Plan = apps.get_model('billing', 'Plan')
    Plan.objects.get_or_create(name='free', defaults={'max_projects': 3})
    Plan.objects.get_or_create(name='pro', defaults={'max_projects': None})


def unseed_plans(apps, schema_editor):
    Plan = apps.get_model('billing', 'Plan')
    Plan.objects.filter(name__in=['free', 'pro']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_plans, unseed_plans),
    ]
