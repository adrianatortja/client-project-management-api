import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_backfill_project_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='projects',
                to='orgs.organization',
            ),
        ),
    ]
