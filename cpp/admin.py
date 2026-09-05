from django.contrib import admin
from .models import Inscription, Resultat

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'classe', 'matricule')
    search_fields = ('nom_complet', 'matricule')
    list_filter = ('classe',)

@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'note_obtenue', 'maximum')
    list_filter = ('matiere',)
