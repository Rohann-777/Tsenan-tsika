"""
Tests unitaires pour le module Dijkstra et sa baseline naïve.

Ces tests vérifient la correction des deux implémentations sur
des graphes représentatifs du réseau routier malgache, et mesurent
le gain de performance du Dijkstra avec tas binaire par rapport
à la version naïve avec recherche linéaire.
"""

import time
import random
from src.backend.algorithms.dijkstra import Dijkstra, DijkstraNaif


def creer_graphe_madagascar():
    """
    Crée un graphe représentant le réseau routier simplifié entre
    les 7 villes pilotes de Tsenan'tsika avec des coûts de transport
    réalistes basés sur les distances approximatives.
    """
    return {
        'Antananarivo': [
            ('Toamasina', 350),
            ('Antsirabe', 170),
            ('Mahajanga', 570),
            ('Fianarantsoa', 410)
        ],
        'Toamasina': [
            ('Antananarivo', 350)
        ],
        'Antsirabe': [
            ('Antananarivo', 170),
            ('Fianarantsoa', 240)
        ],
        'Mahajanga': [
            ('Antananarivo', 570),
            ('Antsiranana', 800)
        ],
        'Fianarantsoa': [
            ('Antananarivo', 410),
            ('Antsirabe', 240),
            ('Toliara', 410)
        ],
        'Toliara': [
            ('Fianarantsoa', 410)
        ],
        'Antsiranana': [
            ('Mahajanga', 800)
        ]
    }


def test_dijkstra_chemin_direct():
    """
    Vérifie que Dijkstra trouve correctement le chemin direct entre
    deux villes voisines, qui devrait simplement être l'arête directe.
    """
    d = Dijkstra()
    graphe = creer_graphe_madagascar()
    
    resultat = d.calculer_chemin_optimal(graphe, 'Antananarivo', 'Antsirabe')
    
    assert resultat['atteignable'] is True
    assert resultat['cout_total'] == 170
    assert resultat['chemin'] == ['Antananarivo', 'Antsirabe']


def test_dijkstra_chemin_avec_escale():
    """
    Vérifie que Dijkstra trouve correctement un chemin qui nécessite
    plusieurs étapes intermédiaires.
    """
    d = Dijkstra()
    graphe = creer_graphe_madagascar()
    
    resultat = d.calculer_chemin_optimal(graphe, 'Toamasina', 'Toliara')
    
    assert resultat['atteignable'] is True
    # Le chemin doit passer par Antananarivo et Fianarantsoa
    assert 'Antananarivo' in resultat['chemin']
    assert 'Fianarantsoa' in resultat['chemin']
    # Coût attendu : Toamasina vers Antananarivo (350) + Antananarivo vers Fianarantsoa (410) + Fianarantsoa vers Toliara (410) = 1170
    assert resultat['cout_total'] == 1170


def test_dijkstra_choisit_chemin_optimal():
    """
    Vérifie que Dijkstra choisit bien le chemin de moindre coût quand
    plusieurs chemins existent entre deux villes.
    
    Pour aller d'Antsirabe à Antananarivo, il y a deux possibilités :
    direct avec un coût de 170, ou via Fianarantsoa avec un coût
    bien plus élevé. Dijkstra doit choisir le chemin direct.
    """
    d = Dijkstra()
    graphe = creer_graphe_madagascar()
    
    resultat = d.calculer_chemin_optimal(graphe, 'Antsirabe', 'Antananarivo')
    
    assert resultat['atteignable'] is True
    assert resultat['cout_total'] == 170
    assert resultat['chemin'] == ['Antsirabe', 'Antananarivo']


def test_dijkstra_meme_sommet():
    """
    Vérifie le cas particulier où le sommet de départ est aussi le
    sommet d'arrivée. Le coût doit être zéro et le chemin contenir
    uniquement ce sommet.
    """
    d = Dijkstra()
    graphe = creer_graphe_madagascar()
    
    resultat = d.calculer_chemin_optimal(graphe, 'Antananarivo', 'Antananarivo')
    
    assert resultat['atteignable'] is True
    assert resultat['cout_total'] == 0
    assert resultat['chemin'] == ['Antananarivo']


def test_coherence_dijkstra_et_naif():
    """
    Vérifie que les deux implémentations produisent toujours les
    mêmes résultats sur les mêmes graphes. C'est crucial car la
    version optimisée doit être strictement équivalente à la baseline.
    """
    d = Dijkstra()
    naif = DijkstraNaif()
    graphe = creer_graphe_madagascar()
    
    paires_test = [
        ('Toamasina', 'Toliara'),
        ('Antsiranana', 'Toliara'),
        ('Mahajanga', 'Fianarantsoa'),
        ('Antananarivo', 'Antsiranana')
    ]
    
    for depart, arrivee in paires_test:
        resultat_d = d.calculer_chemin_optimal(graphe, depart, arrivee)
        resultat_naif = naif.calculer_chemin_optimal(graphe, depart, arrivee)
        
        assert resultat_d['cout_total'] == resultat_naif['cout_total']
        assert resultat_d['atteignable'] == resultat_naif['atteignable']


def test_performance_dijkstra_vs_naif():
    """
    Mesure le temps d'exécution des deux implémentations sur un grand
    graphe généré aléatoirement. Ce test démontre le gain de performance
    apporté par l'utilisation du tas binaire quand le nombre de villes
    augmente, ce qui est crucial pour la scalabilité de Tsenan'tsika
    vers les 114 districts.
    """
    nombre_sommets = 500
    
    # Génération d'un graphe aléatoire dense
    random.seed(42)
    graphe = {}
    for i in range(nombre_sommets):
        graphe[i] = []
    
    for i in range(nombre_sommets):
        # Chaque sommet est connecté à environ 10 autres sommets aléatoires
        for _ in range(10):
            voisin = random.randint(0, nombre_sommets - 1)
            if voisin != i:
                cout = random.randint(1, 1000)
                graphe[i].append((voisin, cout))
    
    d = Dijkstra()
    naif = DijkstraNaif()
    
    # Mesure du Dijkstra avec tas binaire
    debut_d = time.perf_counter()
    d.calculer_chemin_optimal(graphe, 0, nombre_sommets - 1)
    fin_d = time.perf_counter()
    
    # Mesure du Dijkstra naïf
    debut_naif = time.perf_counter()
    naif.calculer_chemin_optimal(graphe, 0, nombre_sommets - 1)
    fin_naif = time.perf_counter()
    
    temps_d = fin_d - debut_d
    temps_naif = fin_naif - debut_naif
    
    print(f"\nTemps Dijkstra avec tas binaire : {temps_d:.6f} secondes")
    print(f"Temps Dijkstra naïf : {temps_naif:.6f} secondes")
    if temps_d > 0:
        gain = temps_naif / temps_d
        print(f"Gain de performance : {gain:.2f}x plus rapide")