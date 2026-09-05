from django.db import models

OPTIONS = ["Scientifique", "Commerciale", "Littéraire", "Pédagogie", "Hôtellerie", "Coupe et Couture"]

CLASSES = []

# Maternelle - pas de A/B
for c in ["1ère Maternelle", "2ème Maternelle", "3ème Maternelle"]:
    CLASSES.append((c, c))

# Primaire 1ère - 6ème -> A, B, C auto
for niv in ["1ère", "2ème", "3ème", "4ème", "5ème", "6ème"]:
    for l in [" A", " B", " C"]:
        CLASSES.append((f"{niv} Primaire{l}", f"{niv} Primaire{l}"))

# Secondaire 7ème, 8ème -> A, B auto seulement
for niv in ["7ème", "8ème"]:
    for l in [" A", " B"]:
        CLASSES.append((f"{niv}{l}", f"{niv}{l}"))

# Humanités 1ère - 6ème avec OPTIONS -> A, B, C auto
for niv in ["1ère", "2ème", "3ème", "4ème", "5ème", "6ème"]:
    for opt in OPTIONS:
        for l in [" A", " B", " C"]:
            CLASSES.append((f"{niv} {opt}{l}", f"{niv} {opt}{l}"))

class Inscription(models.Model):
    nom_complet = models.CharField(max_length=100)
    classe = models.CharField(max_length=50, choices=CLASSES)
    matricule = models.CharField(max_length=50, unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.matricule} - {self.classe}"

class Resultat(models.Model):
    eleve = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    matiere = models.CharField(max_length=50)
    note_obtenue = models.FloatField()
    maximum = models.FloatField(default=20)