import time
import random
from src.backend.algorithms.fenwick_tree import FenwickTree, TableauNaif


def test_fenwick_tree_somme_simple():
    ft = FenwickTree(10)
    ft.mettre_a_jour(0, 100)
    ft.mettre_a_jour(1, 200)
    ft.mettre_a_jour(2, 150)
    
    assert ft.somme_intervalle(0, 2) == 450


def test_fenwick_tree_moyenne_correcte():
    ft = FenwickTree(7)
    prix_semaine = [3500, 3600, 3550, 3700, 3650, 3500, 3450]
    for jour, prix in enumerate(prix_semaine):
        ft.mettre_a_jour(jour, prix)
    
    moyenne = ft.calculer_moyenne(0, 6)
    moyenne_attendue = sum(prix_semaine) / len(prix_semaine)
    
    assert abs(moyenne - moyenne_attendue) < 0.01


def test_fenwick_tree_mise_a_jour_multiple():
    ft = FenwickTree(5)
    ft.mettre_a_jour(2, 100)
    ft.mettre_a_jour(2, 50)
    ft.mettre_a_jour(2, 25)
    
    assert ft.somme_intervalle(2, 2) == 175


def test_coherence_fenwick_et_naif():
    taille = 50
    ft = FenwickTree(taille)
    naif = TableauNaif(taille)
    
    random.seed(42)
    for _ in range(30):
        index = random.randint(0, taille - 1)
        valeur = random.randint(100, 5000)
        ft.mettre_a_jour(index, valeur)
        naif.mettre_a_jour(index, valeur)
    
    intervalles_a_tester = [(0, 9), (10, 25), (5, 30), (0, 49), (20, 35)]
    for debut, fin in intervalles_a_tester:
        somme_ft = ft.somme_intervalle(debut, fin)
        somme_naif = naif.somme_intervalle(debut, fin)
        assert somme_ft == somme_naif


def test_performance_fenwick_vs_naif():
    taille = 10000
    ft = FenwickTree(taille)
    naif = TableauNaif(taille)
    
    random.seed(42)
    valeurs_initiales = [(random.randint(0, taille - 1), random.randint(100, 5000)) 
                         for _ in range(5000)]
    
    for index, valeur in valeurs_initiales:
        ft.mettre_a_jour(index, valeur)
        naif.mettre_a_jour(index, valeur)
    
    requetes = [(random.randint(0, taille // 2), random.randint(taille // 2, taille - 1)) 
                for _ in range(1000)]
    
    debut_ft = time.perf_counter()
    for debut, fin in requetes:
        ft.somme_intervalle(debut, fin)
    fin_ft = time.perf_counter()
    
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
    
    for debut, fin in requetes[:10]:
        assert ft.somme_intervalle(debut, fin) == naif.somme_intervalle(debut, fin)