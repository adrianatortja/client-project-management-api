import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_task_completed_task_created_at_task_description'),
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='projects',
                to='orgs.organization',
            ),
        ),
        migrations.RenameField(
            model_name='project',
            old_name='user',
            new_name='created_by',
        ),
        migrations.AlterField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='created_projects',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
