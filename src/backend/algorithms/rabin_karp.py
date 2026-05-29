class RabinKarp:
    def __init__(self, base=256, modulo=101):
        self.base = base
        self.modulo = modulo

    def normaliser_rapport(self, produit, ville, prix, date_heure):
        produit_norm = produit.strip().lower()
        ville_norm = ville.strip().lower()
        date_norm = date_heure.strftime("%Y%m%d%H")
        return f"{produit_norm}_{ville_norm}_{prix}_{date_norm}"

    def calculer_hachage(self, chaine):
        hachage = 0
        for caractere in chaine:
            hachage = (hachage * self.base + ord(caractere)) % self.modulo
        return hachage

    def verifier_doublon(self, nouveau_rapport, rapports_existants):
        chaine_nouveau = self.normaliser_rapport(
            nouveau_rapport["produit"],
            nouveau_rapport["ville"],
            nouveau_rapport["prix"],
            nouveau_rapport["date_heure"],
        )
        hachage_nouveau = self.calculer_hachage(chaine_nouveau)

        for rapport in rapports_existants:
            chaine_existante = self.normaliser_rapport(
                rapport["produit"],
                rapport["ville"],
                rapport["prix"],
                rapport["date_heure"],
            )
            hachage_existant = self.calculer_hachage(chaine_existante)

            if hachage_nouveau == hachage_existant:
                if chaine_nouveau == chaine_existante:
                    return True
        return False

    def verifier_doublon_avec_cache(self, nouveau_rapport, hachages_existants_avec_chaines):
        chaine_nouveau = self.normaliser_rapport(
            nouveau_rapport["produit"],
            nouveau_rapport["ville"],
            nouveau_rapport["prix"],
            nouveau_rapport["date_heure"],
        )
        hachage_nouveau = self.calculer_hachage(chaine_nouveau)

        for hachage_existant, chaine_existante in hachages_existants_avec_chaines:
            if hachage_nouveau == hachage_existant:
                if chaine_nouveau == chaine_existante:
                    return True

        return False


class DetecteurDoublonNaif:
    def normaliser_rapport(self, produit, ville, prix, date_heure):
        produit_norm = produit.strip().lower()
        ville_norm = ville.strip().lower()
        date_norm = date_heure.strftime("%Y%m%d%H")
        return f"{produit_norm}_{ville_norm}_{prix}_{date_norm}"

    def verifier_doublon(self, nouveau_rapport, rapports_existants):
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

            if chaine_nouveau == chaine_existante:
                return True

        return False

