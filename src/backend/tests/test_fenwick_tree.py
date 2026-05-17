"""
Tests unitaires pour le module Fenwick Tree et sa baseline naïve.

Ces tests vérifient la correction des deux implémentations et mesurent
le gain de performance du Fenwick Tree par rapport à la solution naïve.
Les résultats alimentent le dossier algorithmique pour justifier le
choix de cette structure de données dans Tsenan'tsika.
"""

import time
import random
from src.backend.algorithms.fenwick_tree import FenwickTree, TableauNaif


def test_fenwick_tree_somme_simple():
    """
    Vérifie que le Fenwick Tree calcule correctement la somme d'un
    intervalle simple après quelques insertions.
    """
    ft = FenwickTree(10)
    ft.mettre_a_jour(0, 100)
    ft.mettre_a_jour(1, 200)
    ft.mettre_a_jour(2, 150)
    
    # Somme des trois premiers éléments
    assert ft.somme_intervalle(0, 2) == 450


def test_fenwick_tree_moyenne_correcte():
    """
    Vérifie que le calcul de moyenne fonctionne correctement et
    correspond au cas d'usage de Tsenan'tsika pour la moyenne des
    prix sur une période donnée.
    """
    ft = FenwickTree(7)
    prix_semaine = [3500, 3600, 3550, 3700, 3650, 3500, 3450]
    for jour, prix in enumerate(prix_semaine):
        ft.mettre_a_jour(jour, prix)
    
    moyenne = ft.calculer_moyenne(0, 6)
    moyenne_attendue = sum(prix_semaine) / len(prix_semaine)
    
    # On compare avec une tolérance car on manipule des flottants
    assert abs(moyenne - moyenne_attendue) < 0.01


def test_fenwick_tree_mise_a_jour_multiple():
    """
    Vérifie que plusieurs mises à jour successives sur le même index
    cumulent correctement les valeurs. Ce cas correspond au scénario
    où plusieurs prix sont saisis pour le même jour.
    """
    ft = FenwickTree(5)
    ft.mettre_a_jour(2, 100)
    ft.mettre_a_jour(2, 50)
    ft.mettre_a_jour(2, 25)
    
    assert ft.somme_intervalle(2, 2) == 175


def test_coherence_fenwick_et_naif():
    """
    Vérifie que le Fenwick Tree et la solution naïve produisent
    toujours les mêmes résultats sur les mêmes données. C'est crucial
    car la version optimisée doit être strictement équivalente à la
    baseline en termes de résultat.
    """
    taille = 50
    ft = FenwickTree(taille)
    naif = TableauNaif(taille)
    
    # On effectue les mêmes mises à jour sur les deux structures
    random.seed(42)
    for _ in range(30):
        index = random.randint(0, taille - 1)
        valeur = random.randint(100, 5000)
        ft.mettre_a_jour(index, valeur)
        naif.mettre_a_jour(index, valeur)
    
    # On vérifie que les sommes correspondent sur différents intervalles
    intervalles_a_tester = [(0, 9), (10, 25), (5, 30), (0, 49), (20, 35)]
    for debut, fin in intervalles_a_tester:
        somme_ft = ft.somme_intervalle(debut, fin)
        somme_naif = naif.somme_intervalle(debut, fin)
        assert somme_ft == somme_naif


def test_performance_fenwick_vs_naif():
    """
    Mesure le temps d'exécution des deux implémentations sur un grand
    volume de données avec un mélange d'opérations de mise à jour et
    de requêtes de somme. Ce scénario reflète l'usage réel de Tsenan'tsika
    où les agents saisissent des prix et où le tableau de bord interroge
    régulièrement les moyennes.
    """
    taille = 10000
    ft = FenwickTree(taille)
    naif = TableauNaif(taille)
    
    # Initialisation des deux structures avec les mêmes données
    random.seed(42)
    valeurs_initiales = [(random.randint(0, taille - 1), random.randint(100, 5000)) 
                         for _ in range(5000)]
    
    for index, valeur in valeurs_initiales:
        ft.mettre_a_jour(index, valeur)
        naif.mettre_a_jour(index, valeur)
    
    # Génération des requêtes à exécuter pour la mesure
    requetes = [(random.randint(0, taille // 2), random.randint(taille // 2, taille - 1)) 
                for _ in range(1000)]
    
    # Mesure du Fenwick Tree
    debut_ft = time.perf_counter()
    for debut, fin in requetes:
        ft.somme_intervalle(debut, fin)
    fin_ft = time.perf_counter()
    
    # Mesure de la solution naïve
    debut_naif = time.perf_counter()
    for debut, fin in requetes:
        naif.somme_intervalle(debut, fin)
    fin_naif = time.perf_counter()
    
    temps_ft = fin_ft - debut_ft
    temps_naif = fin_naif - debut_naif
    
    print(f"\nTemps Fenwick Tree : {temps_ft:.6f} secondes")
    print(f"Temps Naïf : {temps_naif:.6f} secondes")
    if temps_ft > 0:
        gain = temps_naif / temps_ft
        print(f"Gain de performance : {gain:.2f}x plus rapide")
    
    # Vérification que les deux donnent les mêmes résultats
    for debut, fin in requetes[:10]:
        assert ft.somme_intervalle(debut, fin) == naif.somme_intervalle(debut, fin)