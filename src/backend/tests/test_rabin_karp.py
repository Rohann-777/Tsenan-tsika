"""
Tests unitaires pour le module Rabin-Karp et sa baseline naïve.

Ces tests vérifient la correction de l'implémentation et mesurent
le gain de performance par rapport à la solution naïve. Les résultats
de performance seront intégrés dans le dossier algorithmique pour
justifier le choix de l'algorithme.
"""

import time
from datetime import datetime, timedelta
from src.backend.algorithms.rabin_karp import RabinKarp, DetecteurDoublonNaif


def generer_rapport(produit, ville, prix, heures_avant=0):
    """
    Fonction utilitaire pour créer un rapport de test avec une date
    décalée d'un certain nombre d'heures par rapport à maintenant.
    Cela facilite la création de jeux de données pour les tests.
    """
    return {
        "produit": produit,
        "ville": ville,
        "prix": prix,
        "date_heure": datetime.now() - timedelta(hours=heures_avant),
    }


def test_rabin_karp_detecte_doublon_simple():
    """
    Vérifie que Rabin-Karp détecte correctement un doublon évident
    quand deux rapports identiques sont soumis.
    """
    rk = RabinKarp()
    rapport = generer_rapport("riz", "antananarivo", 3500)
    existants = [generer_rapport("riz", "antananarivo", 3500)]

    assert rk.verifier_doublon(rapport, existants) is True


def test_rabin_karp_accepte_rapport_unique():
    """
    Vérifie que Rabin-Karp ne déclare pas à tort un doublon quand
    le nouveau rapport est différent de tous les existants.
    """
    rk = RabinKarp()
    rapport = generer_rapport("riz", "antananarivo", 3500)
    existants = [
        generer_rapport("mais", "toamasina", 2800),
        generer_rapport("manioc", "fianarantsoa", 1500),
    ]

    assert rk.verifier_doublon(rapport, existants) is False


def test_rabin_karp_normalisation_casse():
    """
    Vérifie que la normalisation transforme bien la casse et les espaces
    pour que des saisies légèrement différentes du même rapport soient
    bien identifiées comme doublons.
    """
    rk = RabinKarp()
    rapport = generer_rapport("RIZ", "Antananarivo", 3500)
    existants = [generer_rapport("riz", "antananarivo  ", 3500)]

    assert rk.verifier_doublon(rapport, existants) is True


def test_rabin_karp_distingue_prix_differents():
    """
    Vérifie que deux rapports identiques sauf pour le prix sont bien
    considérés comme distincts. C'est important pour ne pas bloquer
    des saisies légitimes de prix qui varient.
    """
    rk = RabinKarp()
    rapport = generer_rapport("riz", "antananarivo", 3500)
    existants = [generer_rapport("riz", "antananarivo", 3600)]

    assert rk.verifier_doublon(rapport, existants) is False


def test_coherence_rabin_karp_et_naif():
    """
    Vérifie que les deux implémentations produisent toujours le même
    résultat sur les mêmes entrées. C'est crucial car la solution
    optimisée doit être strictement équivalente à la baseline en
    termes de résultat.
    """
    rk = RabinKarp()
    naif = DetecteurDoublonNaif()

    cas_de_test = [
        (
            generer_rapport("riz", "antananarivo", 3500),
            [generer_rapport("riz", "antananarivo", 3500)],
        ),
        (
            generer_rapport("mais", "toamasina", 2800),
            [generer_rapport("riz", "antananarivo", 3500)],
        ),
        (generer_rapport("manioc", "fianarantsoa", 1500), []),
    ]

    for nouveau, existants in cas_de_test:
        resultat_rk = rk.verifier_doublon(nouveau, existants)
        resultat_naif = naif.verifier_doublon(nouveau, existants)
        assert resultat_rk == resultat_naif


def test_performance_rabin_karp_vs_naif():
    """
    Mesure le temps d'exécution des deux implémentations dans le scénario
    réel d'usage où Rabin-Karp utilise des hachages précalculés stockés
    en base de données. Cette mesure correspond à ce qui se passe quand
    le système reçoit un nouveau rapport et doit vérifier rapidement
    s'il est un doublon parmi les rapports des dernières 24h.
    """
    rk = RabinKarp()
    naif = DetecteurDoublonNaif()
    
    # Génération de mille rapports existants pour simuler une charge
    # réaliste du système Tsenan'tsika
    rapports_existants = [
        generer_rapport(
            f"produit_{i % 7}",
            f"ville_{i % 7}",
            1000 + i,
            heures_avant=i % 24,
        )
        for i in range(1000)
    ]
    
    # Précalcul des hachages comme cela se ferait en base de données
    # Cette étape est faite une seule fois à l'insertion de chaque rapport
    # et n'est pas comptée dans le temps de vérification de doublon
    hachages_precalcules = []
    for rapport in rapports_existants:
        chaine = rk.normaliser_rapport(
            rapport["produit"],
            rapport["ville"],
            rapport["prix"],
            rapport["date_heure"],
        )
        hachage = rk.calculer_hachage(chaine)
        hachages_precalcules.append((hachage, chaine))
    
    nouveau_rapport = generer_rapport("riz_test", "ville_test", 9999)
    
    # Mesure de Rabin-Karp avec hachages précalculés
    debut_rk = time.perf_counter()
    for _ in range(100):
        rk.verifier_doublon_avec_cache(nouveau_rapport, hachages_precalcules)
    fin_rk = time.perf_counter()
    
    # Mesure de la solution naïve qui recompare tout à chaque fois
    debut_naif = time.perf_counter()
    for _ in range(100):
        naif.verifier_doublon(nouveau_rapport, rapports_existants)
    fin_naif = time.perf_counter()
    
    temps_rk = (fin_rk - debut_rk) / 100
    temps_naif = (fin_naif - debut_naif) / 100
    
    print(f"\nTemps moyen Rabin-Karp avec cache : {temps_rk:.6f} secondes")
    print(f"Temps moyen Naïf : {temps_naif:.6f} secondes")
    if temps_rk > 0:
        gain = temps_naif / temps_rk
        print(f"Gain de performance : {gain:.2f}x plus rapide")
    
    assert rk.verifier_doublon_avec_cache(
        nouveau_rapport, hachages_precalcules
    ) == naif.verifier_doublon(nouveau_rapport, rapports_existants)