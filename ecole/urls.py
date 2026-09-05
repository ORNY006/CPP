from django.contrib import admin
from django.urls import path
from cpp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('inscrire/', views.inscrire, name='inscrire'),
    path('reinscrire/', views.reinscrire, name='reinscrire'),
    path('resultat/', views.resultat, name='resultat'),
    path('a_propos/', views.a_propos, name='a_propos'),
]