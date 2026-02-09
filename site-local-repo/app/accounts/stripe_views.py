import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request):
    user: User = request.user

    # Create/find Stripe customer
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(email=user.email)
        user.stripe_customer_id = customer["id"]
        user.save(update_fields=["stripe_customer_id"])

    success_url = f"{settings.SITE_URL}/subscription/success/"
    cancel_url = f"{settings.SITE_URL}/subscription/cancel/"

    session = stripe.checkout.Session.create(
        mode="subscription",
        customer=user.stripe_customer_id,
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        allow_promotion_codes=True,
    )
    return redirect(session.url, code=303)


@login_required
def subscription_success(request):
    return redirect("home")


@login_required
def subscription_cancel(request):
    return redirect("support")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        return HttpResponse(status=400)

    event_type = event["type"]
    data = event["data"]["object"]

    # 1) Subscription created/updated
    if event_type in ("customer.subscription.created", "customer.subscription.updated"):
        sub = data
        customer_id = sub.get("customer", "")
        status = sub.get("status", "")
        current_period_end = sub.get("current_period_end")

        user = User.objects.filter(stripe_customer_id=customer_id).first()
        if user:
            user.stripe_subscription_id = sub.get("id", "")
            if status in ("active", "trialing"):
                user.is_pro = True
                if current_period_end:
                    user.pro_until = timezone.datetime.fromtimestamp(current_period_end, tz=timezone.utc)
            else:
                user.is_pro = False
                user.pro_until = None
            user.save(update_fields=["stripe_subscription_id", "is_pro", "pro_until"])

    # 2) Subscription cancelled / ended
    if event_type in ("customer.subscription.deleted",):
        sub = data
        customer_id = sub.get("customer", "")
        user = User.objects.filter(stripe_customer_id=customer_id).first()
        if user:
            user.is_pro = False
            user.pro_until = None
            user.stripe_subscription_id = ""
            user.save(update_fields=["stripe_subscription_id", "is_pro", "pro_until"])

    return HttpResponse(status=200)
