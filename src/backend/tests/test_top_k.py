"""
Tests unitaires pour le module Top-k et sa baseline naïve.

Ces tests vérifient la correction de l'implémentation du tas binaire
et démontrent le gain de performance par rapport à l'approche naïve
qui retrie l'ensemble des données à chaque requête.
"""

import time
import random
from src.backend.algorithms.top_k import TopK, TopKNaif


def test_top_k_remplissage_initial():
    """
    Vérifie que le Top-k accepte correctement les premières variations
    quand le tas n'est pas encore plein, sans rien rejeter.
    """
    top = TopK(k=5)
    variations = [(1, 10), (2, 20), (3, 15), (4, 25), (5, 30)]
    
    for produit_id, variation in variations:
        top.mettre_a_jour(produit_id, variation)
    
    # Le tas doit contenir les 5 variations
    resultat = top.get_top_5_hausses()
    assert len(resultat) == 5


def test_top_k_remplace_plus_petite_valeur():
    """
    Vérifie que quand le tas est plein et qu'une nouvelle variation
    plus grande arrive, elle remplace bien la plus petite des variations
    actuellement stockées.
    """
    top = TopK(k=3)
    
    # On remplit le tas avec trois variations
    top.mettre_a_jour(1, 10)
    top.mettre_a_jour(2, 20)
    top.mettre_a_jour(3, 30)
    
    # On ajoute une variation plus grande que la plus petite (10)
    top.mettre_a_jour(4, 25)
    
    resultat = top.get_top_5_hausses()
    valeurs = [v for v, _ in resultat]
    
    # La valeur 10 doit avoir été remplacée par 25
    assert 10 not in valeurs
    assert 25 in valeurs


def test_top_k_ignore_valeur_trop_petite():
    """
    Vérifie que quand le tas est plein et qu'une variation plus petite
    que la racine arrive, elle est ignorée et ne perturbe pas le top.
    """
    top = TopK(k=3)
    
    top.mettre_a_jour(1, 100)
    top.mettre_a_jour(2, 200)
    top.mettre_a_jour(3, 300)
    
    # On ajoute une variation plus petite que toutes les autres
    top.mettre_a_jour(4, 50)
    
    resultat = top.get_top_5_hausses()
    valeurs = [v for v, _ in resultat]
    
    # La valeur 50 ne doit pas être présente
    assert 50 not in valeurs
    # Les trois grandes valeurs doivent toujours être là
    assert set(valeurs) == {100, 200, 300}


def test_top_k_ordre_decroissant():
    """
    Vérifie que get_top_5_hausses retourne bien les variations triées
    par ordre décroissant, ce qui est important pour l'affichage dans
    le tableau de bord.
    """
    top = TopK(k=5)
    
    # On insère les variations dans un ordre aléatoire
    variations_inserees = [15, 80, 30, 90, 45, 60, 20, 75]
    for i, v in enumerate(variations_inserees):
        top.mettre_a_jour(i, v)
    
    resultat = top.get_top_5_hausses()
    valeurs = [v for v, _ in resultat]
    
    # Les valeurs doivent être triées par ordre décroissant
    assert valeurs == sorted(valeurs, reverse=True)
    # Et correspondre aux 5 plus grandes
    assert valeurs == [90, 80, 75, 60, 45]


def test_coherence_top_k_et_naif():
    """
    Vérifie que le Top-k avec tas binaire et la solution naïve
    produisent toujours les mêmes résultats. C'est crucial car la
    version optimisée doit être strictement équivalente à la baseline
    en termes de résultat final.
    """
    top = TopK(k=5)
    naif = TopKNaif(k=5)
    
    random.seed(42)
    for i in range(100):
        variation = random.uniform(0, 1000)
        top.mettre_a_jour(i, variation)
        naif.mettre_a_jour(i, variation)
    
    resultat_top = top.get_top_5_hausses()
    resultat_naif = naif.get_top_5_hausses()
    
    # On compare uniquement les valeurs de variation
    valeurs_top = sorted([v for v, _ in resultat_top], reverse=True)
    valeurs_naif = sorted([v for v, _ in resultat_naif], reverse=True)
    
    assert valeurs_top == valeurs_naif


def test_performance_top_k_vs_naif():
    """
    Mesure le temps d'exécution des deux implémentations sur un grand
    volume de variations. Le scénario simule l'arrivée continue de
    nouvelles variations de prix dans Tsenan'tsika, avec des consultations
    régulières du top par le tableau de bord.
    """
    nombre_variations = 100000
    nombre_consultations = 100
    k = 5
    
    top = TopK(k=k)
    naif = TopKNaif(k=k)
    
    random.seed(42)
    variations = [(i, random.uniform(0, 10000)) for i in range(nombre_variations)]
    
    # Mesure du Top-k avec tas binaire
    debut_top = time.perf_counter()
    for produit_id, variation in variations:
        top.mettre_a_jour(produit_id, variation)
    for _ in range(nombre_consultations):
        top.get_top_5_hausses()
    fin_top = time.perf_counter()
    
    # Mesure de la solution naïve
    debut_naif = time.perf_counter()
    for produit_id, variation in variations:
        naif.mettre_a_jour(produit_id, variation)
    for _ in range(nombre_consultations):
        naif.get_top_5_hausses()
    fin_naif = time.perf_counter()
    
    temps_top = fin_top - debut_top
    temps_naif = fin_naif - debut_naif
    
    print(f"\nTemps Top-k avec tas binaire : {temps_top:.6f} secondes")
    print(f"Temps Naïf : {temps_naif:.6f} secondes")
    if temps_top > 0:
        gain = temps_naif / temps_top
        print(f"Gain de performance : {gain:.2f}x plus rapide")