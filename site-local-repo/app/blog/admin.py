from django.contrib import admin
from .models import SiteSettings, EntertainmentLink, Category, Article

admin.site.site_header = "Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Control Center"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General", {'fields': ('site_name','logo','background')}),
        ("Home Page Texts", {'fields': (('home_top_text1_en','home_top_text1_uk'),
                                        ('home_top_text2_en','home_top_text2_uk'),
                                        ('home_main_text_en','home_main_text_uk'))}),
        ("About Page", {'fields': ('about_image',('about_text_en','about_text_uk'))}),
        ("Help Page", {'fields': (('help_text_en','help_text_uk'),)}),
        ("Support Page", {'fields': (('support_text_en','support_text_uk'),'support_qr',
                                     ('support_footer_en','support_footer_uk'))}),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists() or super().has_add_permission(request)

@admin.register(EntertainmentLink)
class EntertainmentLinkAdmin(admin.ModelAdmin):
    list_display = ('title','url','order')
    list_editable = ('order',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','order','slug')
    list_editable = ('order',)
    ordering = ('order',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','language','published','public','is_pro','order','created_at','likes','dislikes')
    list_editable = ('order','published','public','is_pro')
    list_filter = ('category','language','published','public','is_pro')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','content')
    ordering = ('order','-created_at')
    fieldsets = (
        (None, {'fields': ('category','title','slug','language','content','pdf','is_pro','order','published','public')}),
        ('External buttons (optional)', {'fields': (('link1_label','link1_url'),('link2_label','link2_url'))}),
    )
