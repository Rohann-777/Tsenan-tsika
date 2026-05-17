"""
Module Rabin-Karp pour la détection de rapports dupliqués dans Tsenan'tsika.

Cet algorithme utilise le hachage polynomial avec fenêtre glissante pour
détecter efficacement les rapports identiques soumis dans une fenêtre
temporelle de 24h. Il évite les comparaisons caractère par caractère
coûteuses en comparant d'abord les hachages, puis en confirmant uniquement
en cas de correspondance.

Complexité moyenne : O(n + m) où n est la longueur du texte global
parcouru et m la longueur du motif recherché.
"""


class RabinKarp:
    """
    Implémentation manuelle de l'algorithme Rabin-Karp pour la détection
    de doublons dans les rapports de prix soumis par les agents.
    """

    def __init__(self, base=256, modulo=101):
        """
        Initialise les paramètres du hachage polynomial.

        La base correspond au nombre de caractères possibles que peut
        contenir une chaîne. On utilise 256 car cela couvre tous les
        caractères ASCII étendus, ce qui est suffisant pour nos chaînes
        normalisées.

        Le modulo est un nombre premier utilisé pour éviter que les
        hachages ne deviennent trop grands. Le choix d'un nombre premier
        réduit également la probabilité de collisions.
        """
        self.base = base
        self.modulo = modulo

    def normaliser_rapport(self, produit, ville, prix, date_heure):
        """
        Construit une chaîne normalisée à partir des données d'un rapport.

        La normalisation est essentielle car elle garantit que deux
        rapports identiques produiront exactement la même chaîne, donc
        le même hachage. On arrondit la date à l'heure pour considérer
        comme doublons les rapports soumis dans la même heure.

        Format : "produit_ville_prix_dateheure"
        Exemple : "riz_antananarivo_3500_2026051614"
        """
        # On force tout en minuscules et on retire les espaces pour
        # éviter qu'un agent qui écrit "Riz " et un autre "riz" ne
        # créent deux chaînes différentes pour le même rapport
        produit_norm = produit.strip().lower()
        ville_norm = ville.strip().lower()
        # On arrondit la date à l'heure (format YYYYMMDDHH)
        date_norm = date_heure.strftime("%Y%m%d%H")
        return f"{produit_norm}_{ville_norm}_{prix}_{date_norm}"

    def calculer_hachage(self, chaine):
        """
        Calcule le hachage polynomial d'une chaîne complète.

        La formule est : hachage = (c0 * base^(n-1) + c1 * base^(n-2) +
        ... + cn-1 * base^0) mod modulo, où ci est la valeur ASCII du
        i-ième caractère et n est la longueur de la chaîne.

        Cette formule traite la chaîne comme un nombre dans la base
        donnée, ce qui permet de calculer rapidement le hachage de
        sous-chaînes adjacentes via le hachage roulant.
        """
        hachage = 0
        for caractere in chaine:
            # On multiplie le hachage actuel par la base et on ajoute
            # la valeur ASCII du nouveau caractère, puis on applique
            # le modulo pour garder le résultat dans une plage raisonnable
            hachage = (hachage * self.base + ord(caractere)) % self.modulo
        return hachage

    def verifier_doublon(self, nouveau_rapport, rapports_existants):
        """
        Vérifie si un nouveau rapport est un doublon parmi les rapports
        soumis dans les dernières 24h.

        nouveau_rapport : dictionnaire contenant produit, ville, prix,
                          date_heure du rapport à vérifier
        rapports_existants : liste de dictionnaires similaires représentant
                             les rapports déjà en base dans les 24h

        Retourne True si un doublon est détecté, False sinon.
        """
        # Étape 1 : on normalise et on hache le nouveau rapport
        chaine_nouveau = self.normaliser_rapport(
            nouveau_rapport["produit"],
            nouveau_rapport["ville"],
            nouveau_rapport["prix"],
            nouveau_rapport["date_heure"],
        )
        hachage_nouveau = self.calculer_hachage(chaine_nouveau)

        # Étape 2 : on compare avec chaque rapport existant
        for rapport in rapports_existants:
            chaine_existante = self.normaliser_rapport(
                rapport["produit"],
                rapport["ville"],
                rapport["prix"],
                rapport["date_heure"],
            )
            hachage_existant = self.calculer_hachage(chaine_existante)

            # Première vérification : les hachages correspondent-ils ?
            if hachage_nouveau == hachage_existant:
                # Deuxième vérification : confirmation caractère par
                # caractère pour éviter les faux positifs dus aux
                # collisions de hachage
                if chaine_nouveau == chaine_existante:
                    return True
        return False
                

    def verifier_doublon_avec_cache(self, nouveau_rapport, hachages_existants_avec_chaines):
        """
        Version optimisée qui exploite des hachages précalculés.
        
        Cette méthode correspond au scénario réel d'utilisation dans
        Tsenan'tsika : quand un rapport est inséré en base, son hachage
        est calculé une fois et stocké. Lors d'une vérification de doublon,
        on n'a plus qu'à calculer le hachage du nouveau rapport et le
        comparer avec les hachages déjà stockés.
        
        hachages_existants_avec_chaines : liste de tuples (hachage, chaine_originale)
        représentant les rapports déjà en base avec leur hachage précalculé.
        
        Complexité : O(n + m) où n est le nombre de rapports existants
        et m la longueur de la chaîne du nouveau rapport. Le facteur m
        n'apparaît qu'une fois pour le nouveau rapport, et non pour chaque
        comparaison comme dans la version naïve.
        """
        # On calcule le hachage du nouveau rapport une seule fois
        chaine_nouveau = self.normaliser_rapport(
            nouveau_rapport["produit"],
            nouveau_rapport["ville"],
            nouveau_rapport["prix"],
            nouveau_rapport["date_heure"],
        )
        hachage_nouveau = self.calculer_hachage(chaine_nouveau)
        
        # On compare avec les hachages précalculés des rapports existants
        for hachage_existant, chaine_existante in hachages_existants_avec_chaines:
            if hachage_nouveau == hachage_existant:
                # Vérification de confirmation en cas de collision
                if chaine_nouveau == chaine_existante:
                    return True
    
        return False

class DetecteurDoublonNaif:
    """
    Solution naïve de détection de doublons par comparaison directe
    caractère par caractère. Sert de baseline pour mesurer le gain
    de performance apporté par Rabin-Karp.

    Cette implémentation ne fait aucune optimisation : pour chaque
    nouveau rapport, elle parcourt tous les rapports existants et
    compare les chaînes normalisées caractère par caractère via
    l'opérateur d'égalité standard de Python.

    Complexité : O(n * m) où n est le nombre de rapports existants
    et m la longueur moyenne d'une chaîne normalisée.
    """

    def normaliser_rapport(self, produit, ville, prix, date_heure):
        """
        Construit la même chaîne normalisée que Rabin-Karp pour
        garantir une comparaison équitable entre les deux approches.
        """
        produit_norm = produit.strip().lower()
        ville_norm = ville.strip().lower()
        date_norm = date_heure.strftime("%Y%m%d%H")
        return f"{produit_norm}_{ville_norm}_{prix}_{date_norm}"

    def verifier_doublon(self, nouveau_rapport, rapports_existants):
        """
        Compare directement la chaîne du nouveau rapport avec toutes
        les chaînes existantes, sans utiliser de hachage intermédiaire.
        """
        chaine_nouveau = self.normaliser_rapport(
            nouveau_rapport["produit"],
            nouveau_rapport["ville"],
            nouveau_rapport["prix"],
            nouveau_rapport["date_heure"],
        )

        for rapport in rapports_existants:
            chaine_existante = self.normaliser_rapport(
                rapport["produit"],
                rapport["ville"],
                rapport["prix"],
                rapport["date_heure"],
            )

            # Comparaison directe sans optimisation
            if chaine_nouveau == chaine_existante:
                return True

        return False