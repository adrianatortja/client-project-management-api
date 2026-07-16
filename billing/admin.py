from django.contrib import admin

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'stripe_price_id', 'max_projects')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'plan', 'status', 'current_period_end')
    list_filter = ('status', 'plan')
