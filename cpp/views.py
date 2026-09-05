from django.shortcuts import render
from .models import Inscription, Resultat, CLASSES
from datetime import datetime

MAX = 32

def placer_auto(base):
    base = base.strip()
    if base in ["7ème", "8ème"]:
        for l in [" A", " B"]:
            cand = base + l
            if Inscription.objects.filter(classe=cand).count() < MAX:
                return cand
        return None
    # Primaire et Humanités -> A, B, C
    for l in [" A", " B", " C"]:
        cand = base + l
        if Inscription.objects.filter(classe=cand).count() < MAX:
            return cand
    return None

def accueil(request):
    return render(request, 'accueil.html')

def a_propos(request):
    return render(request, 'a_propos.html')

def inscrire(request):
    message = ""; new_matricule = ""
    if request.method == "POST":
        nom = request.POST.get('nom_complet','').strip()
        niveau = request.POST.get('niveau','').strip()
        section = request.POST.get('section','').strip()

        if not nom or not niveau:
            message = "Remplis tout"
        else:
            if "Maternelle" in niveau:
                classe_finale = niveau
            elif "Primaire" in niveau:
                classe_finale = placer_auto(niveau)
                if not classe_finale:
                    message = f"⛔ BLOQUÉ: {niveau} complet. A,B,C ont déjà 32 élèves."
                    return render(request, 'inscrire.html', {'message': message})
            elif niveau in ["7ème", "8ème"]:
                classe_finale = placer_auto(niveau)
                if not classe_finale:
                    message = f"⛔ BLOQUÉ: {niveau} complet. A et B ont 32."
                    return render(request, 'inscrire.html', {'message': message})
            else: # Humanités 1ère-6ème
                if not section:
                    message = "Choisis l'option: Scientifique, Commerciale, etc."
                    return render(request, 'inscrire.html', {'message': message})
                base_hum = f"{niveau} {section}"
                classe_finale = placer_auto(base_hum)
                if not classe_finale:
                    message = f"⛔ BLOQUÉ: {base_hum} complet. A,B,C ont 32."
                    return render(request, 'inscrire.html', {'message': message})

            if "Maternelle" in classe_finale:
                if Inscription.objects.filter(classe=classe_finale).count() >= MAX:
                    message = f"⛔ BLOQUÉ: {classe_finale} a déjà 32"
                    return render(request, 'inscrire.html', {'message': message})

            from datetime import datetime
            count = Inscription.objects.count() + 1
            annee_debut = datetime.now().year % 100  # 25 pour 2025
            annee_fin = (datetime.now().year + 1) % 100  # 26 pour 2026
            matricule = f"{annee_debut:02d}-CPP-{count:03d}-{annee_fin:02d}"
            Inscription.objects.create(nom_complet=nom, classe=classe_finale, matricule=matricule)
            message = f"✅ {nom} inscrit en {classe_finale}"
            new_matricule = matricule

    return render(request, 'inscrire.html', {'message': message, 'new_matricule': new_matricule})

def reinscrire(request):
    message = ""
    if request.method == "POST":
        matricule = request.POST.get('matricule','').strip().upper()
        niveau = request.POST.get('niveau','').strip()
        section = request.POST.get('section','').strip()
        try:
            eleve = Inscription.objects.get(matricule__iexact=matricule)
            if "Maternelle" in niveau:
                classe_finale = niveau
            elif "Primaire" in niveau:
                classe_finale = placer_auto(niveau)
                if not classe_finale:
                    message = f"⛔ BLOQUÉ: {niveau} Primaire complet."
                    return render(request, 'reinscrire.html', {'message': message})
            elif niveau in ["7ème", "8ème"]:
                classe_finale = placer_auto(niveau)
                if not classe_finale:
                    if eleve.classe.startswith(niveau):
                        classe_finale = eleve.classe
                    else:
                        message = f"⛔ BLOQUÉ: {niveau} complet."
                        return render(request, 'reinscrire.html', {'message': message})
            else:
                base_hum = f"{niveau} {section}"
                classe_finale = placer_auto(base_hum)
                if not classe_finale:
                    if eleve.classe.startswith(base_hum):
                        classe_finale = eleve.classe
                    else:
                        message = f"⛔ BLOQUÉ: {base_hum} complet."
                        return render(request, 'reinscrire.html', {'message': message})

            eleve.classe = classe_finale
            eleve.save()
            message = f"✅ {eleve.nom_complet} réinscrit en {classe_finale}"
        except Inscription.DoesNotExist:
            message = f"⛔ Matricule {matricule} introuvable"
    return render(request, 'reinscrire.html', {'message': message})

def resultat(request):
    eleve=None; resultats=[]; message=""; total_obtenu=0; total_max=0; pourcentage=0; mention=""
    if request.method=="POST":
        matricule=request.POST.get('matricule','').strip().upper()
        try:
            eleve=Inscription.objects.get(matricule__iexact=matricule)
            resultats=Resultat.objects.filter(eleve=eleve)
            for r in resultats:
                total_obtenu+=r.note_obtenue
                total_max+=r.maximum
            if total_max>0:
                pourcentage=round((total_obtenu/total_max)*100,2)
                if pourcentage>=80: mention="Grande Distinction"
                elif pourcentage>=60: mention="Distinction"
                elif pourcentage>=50: mention="Satisfaction"
                else: mention="Ajourné"
        except:
            message=f"Matricule {matricule} introuvable"
    return render(request, 'resultat.html', {'eleve':eleve,'resultats':resultats,'message':message,'total_obtenu':total_obtenu,'total_max':total_max,'pourcentage':pourcentage,'mention':mention})