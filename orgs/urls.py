from django.urls import include, path

from billing import views as billing_views

from . import views

urlpatterns = [
    path('', views.OrganizationListCreateView.as_view(), name='org-list-create'),
    path('<slug:org_slug>/', views.OrganizationDetailView.as_view(), name='org-detail'),
    path('<slug:org_slug>/members/', views.MembershipListView.as_view(), name='org-members'),
    path('<slug:org_slug>/invite/', views.MembershipInviteView.as_view(), name='org-invite'),
    path('<slug:org_slug>/projects/', include('projects.urls')),
    path(
        '<slug:org_slug>/billing/',
        billing_views.SubscriptionDetailView.as_view(),
        name='billing-detail',
    ),
    path(
        '<slug:org_slug>/billing/checkout/',
        billing_views.CreateCheckoutSessionView.as_view(),
        name='billing-checkout',
    ),
    path(
        '<slug:org_slug>/billing/portal/',
        billing_views.CreatePortalSessionView.as_view(),
        name='billing-portal',
    ),
]
