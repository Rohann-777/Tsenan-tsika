import time
import random
import string

from src.backend.algorithms.dijkstra import Dijkstra, DijkstraNaif
from src.backend.algorithms.rabin_karp import RabinKarp, DetecteurDoublonNaif
from src.backend.algorithms.fenwick_tree import FenwickTree, TableauNaif
from src.backend.algorithms.top_k import TopK, TopKNaif


REPETITIONS = 5


def mesurer(fonction, repetitions=REPETITIONS):
    temps_total = 0.0
    for _ in range(repetitions):
        debut = time.perf_counter()
        fonction()
        fin = time.perf_counter()
        temps_total += (fin - debut)
    return temps_total / repetitions


def benchmark_dijkstra():
    nombre_sommets = 2000
    random.seed(42)
    graphe = {i: [] for i in range(nombre_sommets)}
    for i in range(nombre_sommets):
        for _ in range(15):
            voisin = random.randint(0, nombre_sommets - 1)
            if voisin != i:
                graphe[i].append((voisin, random.randint(1, 1000)))

    optimise = Dijkstra()
    naif = DijkstraNaif()
    depart, arrivee = 0, nombre_sommets - 1

    temps_opt = mesurer(lambda: optimise.calculer_chemin_optimal(graphe, depart, arrivee))
    temps_naif = mesurer(lambda: naif.calculer_chemin_optimal(graphe, depart, arrivee))
    return "Dijkstra", temps_naif, temps_opt


def benchmark_rabin_karp():
    from datetime import datetime

    random.seed(42)
    nombre_existants = 2000
    nombre_verifications = 2000
    produits = ["Riz", "Maïs", "Manioc", "Haricot", "Huile", "Sucre", "Sel"]
    villes = ["Antananarivo", "Toamasina", "Antsirabe", "Mahajanga",
              "Fianarantsoa", "Toliara", "Antsiranana"]

    def rapport_aleatoire():
        return {
            "produit": random.choice(produits),
            "ville": random.choice(villes),
            "prix": random.randint(1000, 9000),
            "date_heure": datetime.now()
        }

    rapports_existants = [rapport_aleatoire() for _ in range(nombre_existants)]
    nouveaux_rapports = [rapport_aleatoire() for _ in range(nombre_verifications)]

    optimise = RabinKarp()
    naif = DetecteurDoublonNaif()

    def scenario_naif():
        for nouveau in nouveaux_rapports:
            naif.verifier_doublon(nouveau, rapports_existants)

    def scenario_optimise():
        cache = []
        for rapport in rapports_existants:
            chaine = optimise.normaliser_rapport(
                rapport["produit"], rapport["ville"],
                rapport["prix"], rapport["date_heure"])
            cache.append((optimise.calculer_hachage(chaine), chaine))
        for nouveau in nouveaux_rapports:
            optimise.verifier_doublon_avec_cache(nouveau, cache)

    temps_opt = mesurer(scenario_optimise)
    temps_naif = mesurer(scenario_naif)
    return "Rabin-Karp", temps_naif, temps_opt


def benchmark_fenwick_tree():
    random.seed(42)
    taille = 20000
    valeurs = [random.randint(1000, 9000) for _ in range(taille)]

    def scenario_optimise():
        arbre = FenwickTree(taille)
        for i, v in enumerate(valeurs):
            arbre.mettre_a_jour(i, v)
        # Nombreuses requêtes de moyenne sur intervalles
        for _ in range(5000):
            debut = random.randint(0, taille - 2)
            fin = random.randint(debut, taille - 1)
            arbre.calculer_moyenne(debut, fin)

    def scenario_naif():
        arbre = TableauNaif(taille)
        for i, v in enumerate(valeurs):
            arbre.mettre_a_jour(i, v)
        for _ in range(5000):
            debut = random.randint(0, taille - 2)
            fin = random.randint(debut, taille - 1)
            arbre.calculer_moyenne(debut, fin)

    temps_opt = mesurer(scenario_optimise)
    temps_naif = mesurer(scenario_naif)
    return "Fenwick Tree", temps_naif, temps_opt


def benchmark_top_k():
    random.seed(42)
    nombre_variations = 50000
    variations = [(random.uniform(-50, 50), i) for i in range(nombre_variations)]

    def scenario_optimise():
        topk = TopK(k=5)
        for variation, produit_id in variations:
            topk.mettre_a_jour(produit_id, variation)
        topk.get_top_5_hausses()

    def scenario_naif():
        topk = TopKNaif(k=5)
        for variation, produit_id in variations:
            topk.mettre_a_jour(produit_id, variation)
        topk.get_top_5_hausses()

    temps_opt = mesurer(scenario_optimise)
    temps_naif = mesurer(scenario_naif)
    return "Top-k", temps_naif, temps_opt


def afficher_resultats(resultats):
    print("\n" + "=" * 70)
    print(" BANC D'ESSAI COMPARATIF — TSENAN'TSIKA")
    print(" Algorithmes optimisés vs versions naïves")
    print(f" Moyenne sur {REPETITIONS} exécutions par mesure")
    print("=" * 70)
    print(f"\n{'Algorithme':<16}{'Naïf (ms)':>14}{'Optimisé (ms)':>16}{'Gain':>12}")
    print("-" * 70)

    for nom, temps_naif, temps_opt in resultats:
        naif_ms = temps_naif * 1000
        opt_ms = temps_opt * 1000
        gain = temps_naif / temps_opt if temps_opt > 0 else float('inf')
        print(f"{nom:<16}{naif_ms:>14.3f}{opt_ms:>16.3f}{gain:>10.1f}x")

    print("-" * 70)
    print("\nLecture : « Gain » indique combien de fois la version optimisée")
    print("est plus rapide que la version naïve sur le même problème.\n")


def main():
    print("\nExécution du banc d'essai en cours, veuillez patienter...")
    resultats = [
        benchmark_dijkstra(),
        benchmark_rabin_karp(),
        benchmark_fenwick_tree(),
        benchmark_top_k(),
    ]
    afficher_resultats(resultats)


if __name__ == "__main__":
    main()