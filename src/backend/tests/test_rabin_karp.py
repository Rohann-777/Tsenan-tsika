import time
from datetime import datetime, timedelta
from src.backend.algorithms.rabin_karp import RabinKarp, DetecteurDoublonNaif


def generer_rapport(produit, ville, prix, heures_avant=0):
    return {
        "produit": produit,
        "ville": ville,
        "prix": prix,
        "date_heure": datetime.now() - timedelta(hours=heures_avant),
    }


def test_rabin_karp_detecte_doublon_simple():
    rk = RabinKarp()
    rapport = generer_rapport("riz", "antananarivo", 3500)
    existants = [generer_rapport("riz", "antananarivo", 3500)]

    assert rk.verifier_doublon(rapport, existants) is True


def test_rabin_karp_accepte_rapport_unique():
    rk = RabinKarp()
    rapport = generer_rapport("riz", "antananarivo", 3500)
    existants = [
        generer_rapport("mais", "toamasina", 2800),
        generer_rapport("manioc", "fianarantsoa", 1500),
    ]

    assert rk.verifier_doublon(rapport, existants) is False


def test_rabin_karp_normalisation_casse():
    rk = RabinKarp()
    rapport = generer_rapport("RIZ", "Antananarivo", 3500)
    existants = [generer_rapport("riz", "antananarivo  ", 3500)]

    assert rk.verifier_doublon(rapport, existants) is True


def test_rabin_karp_distingue_prix_differents():
    rk = RabinKarp()
    rapport = generer_rapport("riz", "antananarivo", 3500)
    existants = [generer_rapport("riz", "antananarivo", 3600)]

    assert rk.verifier_doublon(rapport, existants) is False


def test_coherence_rabin_karp_et_naif():
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
    rk = RabinKarp()
    naif = DetecteurDoublonNaif()
    
    rapports_existants = [
        generer_rapport(
            f"produit_{i % 7}",
            f"ville_{i % 7}",
            1000 + i,
            heures_avant=i % 24,
        )
        for i in range(1000)
    ]
    
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

    debut_rk = time.perf_counter()
    for _ in range(100):
        rk.verifier_doublon_avec_cache(nouveau_rapport, hachages_precalcules)
    fin_rk = time.perf_counter()
    
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