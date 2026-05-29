import time
import random
from src.backend.algorithms.top_k import TopK, TopKNaif


def test_top_k_remplissage_initial():
    top = TopK(k=5)
    variations = [(1, 10), (2, 20), (3, 15), (4, 25), (5, 30)]
    
    for produit_id, variation in variations:
        top.mettre_a_jour(produit_id, variation)
    
    resultat = top.get_top_5_hausses()
    assert len(resultat) == 5


def test_top_k_remplace_plus_petite_valeur():
    top = TopK(k=3)
    
    top.mettre_a_jour(1, 10)
    top.mettre_a_jour(2, 20)
    top.mettre_a_jour(3, 30)
    
    top.mettre_a_jour(4, 25)
    
    resultat = top.get_top_5_hausses()
    valeurs = [v for v, _ in resultat]
    
    assert 10 not in valeurs
    assert 25 in valeurs


def test_top_k_ignore_valeur_trop_petite():
    top = TopK(k=3)
    
    top.mettre_a_jour(1, 100)
    top.mettre_a_jour(2, 200)
    top.mettre_a_jour(3, 300)
    
    top.mettre_a_jour(4, 50)
    
    resultat = top.get_top_5_hausses()
    valeurs = [v for v, _ in resultat]
    
    assert 50 not in valeurs
    assert set(valeurs) == {100, 200, 300}


def test_top_k_ordre_decroissant():
    top = TopK(k=5)
    
    variations_inserees = [15, 80, 30, 90, 45, 60, 20, 75]
    for i, v in enumerate(variations_inserees):
        top.mettre_a_jour(i, v)
    
    resultat = top.get_top_5_hausses()
    valeurs = [v for v, _ in resultat]
    
    assert valeurs == sorted(valeurs, reverse=True)
    assert valeurs == [90, 80, 75, 60, 45]


def test_coherence_top_k_et_naif():
    top = TopK(k=5)
    naif = TopKNaif(k=5)
    
    random.seed(42)
    for i in range(100):
        variation = random.uniform(0, 1000)
        top.mettre_a_jour(i, variation)
        naif.mettre_a_jour(i, variation)
    
    resultat_top = top.get_top_5_hausses()
    resultat_naif = naif.get_top_5_hausses()
    
    valeurs_top = sorted([v for v, _ in resultat_top], reverse=True)
    valeurs_naif = sorted([v for v, _ in resultat_naif], reverse=True)
    
    assert valeurs_top == valeurs_naif


def test_performance_top_k_vs_naif():
    nombre_variations = 100000
    nombre_consultations = 100
    k = 5
    
    top = TopK(k=k)
    naif = TopKNaif(k=k)
    
    random.seed(42)
    variations = [(i, random.uniform(0, 10000)) for i in range(nombre_variations)]
    
    debut_top = time.perf_counter()
    for produit_id, variation in variations:
        top.mettre_a_jour(produit_id, variation)
    for _ in range(nombre_consultations):
        top.get_top_5_hausses()
    fin_top = time.perf_counter()
    
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