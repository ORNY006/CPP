from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscrire, name='inscription'),
    path('reinscription/', views.reinscrire, name='reinscription'),
    path('resultat/', views.resultat, name='resultat'),
    path('a-propos/', views.a_propos, name='a_propos'),
]