from .models import SiteSettings, EntertainmentLink
from django.utils import timezone


def _pick_lang_pair(obj, base, lang):
    candidate = getattr(obj, f"{base}_{lang}", None)
    if candidate:
        if isinstance(candidate, str) and candidate.strip():
            return candidate
        return candidate
    return getattr(obj, base, "")


def site_settings(request):
    settings_obj = SiteSettings.objects.first()
    entertainment_links = EntertainmentLink.objects.all()
    lang = (getattr(request, "LANGUAGE_CODE", "en") or "en")[:2]

    texts = {}
    if settings_obj:
        for base in [
            "home_top_text1",
            "home_top_text2",
            "home_main_text",
            "about_text",
            "help_text",
        ]:
            texts[base] = _pick_lang_pair(settings_obj, base, lang)

    # Subscription tier
    tier = "FREE"
    if request.user.is_authenticated:
        if getattr(request.user, "is_pro", False):
            tier = "PRO"
        else:
            pro_until = getattr(request.user, "pro_until", None)
            if pro_until and pro_until > timezone.now():
                tier = "PRO"

    return {
        "SITESETTINGS": settings_obj,
        "ENTERTAINMENT_LINKS": entertainment_links,
        "TEXTS": texts,
        "SUBSCRIPTION_TIER": tier,
    }
