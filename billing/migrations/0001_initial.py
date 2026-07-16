import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('free', 'Free'), ('pro', 'Pro')], max_length=50, unique=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=255)),
                ('max_projects', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('active', 'Active'), ('past_due', 'Past due'), ('canceled', 'Canceled')], default='active', max_length=30)),
                ('current_period_end', models.DateTimeField(blank=True, null=True)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='orgs.organization')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='billing.plan')),
            ],
        ),
    ]
