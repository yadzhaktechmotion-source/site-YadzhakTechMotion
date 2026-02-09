from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default="your text")
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text=_("Company logo for top-left navbar"))
    background = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text=_("Site-wide background image"))

    home_top_text1 = models.CharField(max_length=200, blank=True, help_text=_("Short top text (two lines max)"))
    home_top_text2 = models.CharField(max_length=200, blank=True, help_text=_("Short top text (two lines max)"))
    home_main_text = models.TextField(blank=True, help_text=_("Main centered text"))

    about_image = models.ImageField(upload_to='about/', blank=True, null=True)
    about_text = models.TextField(blank=True)

    support_text_en = models.TextField(blank=True, help_text=_("Support page text (EN)"))
    support_text_uk = models.TextField(blank=True, help_text=_("Support page text (UK)"))
    support_qr = models.ImageField(upload_to='support/', blank=True, null=True, help_text=_("QR code image for donations or support"))
    support_footer_en = models.TextField(blank=True, help_text=_("Support footer text (EN)"))
    support_footer_uk = models.TextField(blank=True, help_text=_("Support footer text (UK)"))

    help_text = models.TextField(blank=True, help_text=_("Content for the Help page"))

    home_top_text1_en = models.CharField(max_length=200, blank=True, help_text=_("Short top text (EN)"))
    home_top_text1_uk = models.CharField(max_length=200, blank=True, help_text=_("Short top text (UK)"))

    home_top_text2_en = models.CharField(max_length=200, blank=True, help_text=_("Short top text (EN)"))
    home_top_text2_uk = models.CharField(max_length=200, blank=True, help_text=_("Short top text (UK)"))

    home_main_text_en = models.TextField(blank=True, help_text=_("Main centered text (EN)"))
    home_main_text_uk = models.TextField(blank=True, help_text=_("Main centered text (UK)"))

    about_text_en = models.TextField(blank=True, help_text=_("About page (EN)"))
    about_text_uk = models.TextField(blank=True, help_text=_("About page (UK)"))

    help_text_en = models.TextField(blank=True, help_text=_("Help page (EN)"))
    help_text_uk = models.TextField(blank=True, help_text=_("Help page (UK)"))

    class Meta:
        verbose_name = _("Site settings")
        verbose_name_plural = _("Site settings")

    def __str__(self):
        return "Site Settings"

class EntertainmentLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order','title']
        verbose_name = _("Entertainment link")
        verbose_name_plural = _("Entertainment links")
    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text=_("Determines display order of categories (lower numbers appear first)"))
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['order','name']
    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    language = models.CharField(max_length=2, choices=[('en','EN'),('uk','UA')], default='en')
    content = models.TextField(blank=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    link1_label = models.CharField(max_length=50, blank=True)
    link1_url = models.URLField(blank=True)
    link2_label = models.CharField(max_length=50, blank=True)
    link2_url = models.URLField(blank=True)

    published = models.BooleanField(default=True)
    public = models.BooleanField(default=True, help_text=_("Visible to unauthenticated users"))
    
    is_pro = models.BooleanField(
        default=False,
        help_text=_("Requires PRO subscription")
    )
    
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    order = models.PositiveIntegerField(default=0, help_text="Manual order number for sorting (lower = higher priority)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order','-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        settings = SiteSettings.objects.first()
        if self.pdf and settings and settings.logo:
            try:
                self.pdf = apply_watermark(self.pdf, settings.logo)
            except Exception as e:
                print(" PDF watermark skipped:", e)
        super().save(*args, **kwargs)
