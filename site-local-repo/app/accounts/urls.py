from django.urls import path
from .views import login_or_register, logout_view

from .stripe_views import (
    create_checkout_session,
    subscription_success,
    subscription_cancel,
    stripe_webhook,
)

urlpatterns = [
    # Auth
    path('login/', login_or_register, name='login'),
    path('logout/', logout_view, name='logout'),

    # Subscription / Stripe
    path("subscription/checkout/", create_checkout_session, name="subscription_checkout"),
    path("subscription/success/", subscription_success, name="subscription_success"),
    path("subscription/cancel/", subscription_cancel, name="subscription_cancel"),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
]
