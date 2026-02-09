from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),
    path('support/', views.support, name='support'),
    path('map/', views.devops_map, name='devops_map'),

    # Dynamic routes
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('article/<slug:slug>/pdf/', views.article_pdf_view, name='article_pdf_view'),
    
    # Voting
    path('vote/<int:article_id>/<str:action>/', views.vote_article, name='vote_article'),
]
