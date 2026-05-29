class TopK:
    def __init__(self, k=5):
        self.k = k
        self.tas = []

    def _parent(self, index):
        return (index - 1) // 2

    def _enfant_gauche(self, index):
        return 2 * index + 1

    def _enfant_droit(self, index):
        return 2 * index + 2

    def _percoler_vers_le_haut(self, index):
        while index > 0:
            parent = self._parent(index)
            if self.tas[index][0] < self.tas[parent][0]:
                self.tas[index], self.tas[parent] = self.tas[parent], self.tas[index]
                index = parent
            else:
                break

    def _percoler_vers_le_bas(self, index):
        n = len(self.tas)
        while True:
            gauche = self._enfant_gauche(index)
            droit = self._enfant_droit(index)
            plus_petit = index

            if gauche < n and self.tas[gauche][0] < self.tas[plus_petit][0]:
                plus_petit = gauche
            if droit < n and self.tas[droit][0] < self.tas[plus_petit][0]:
                plus_petit = droit

            if plus_petit == index:
                break

            self.tas[index], self.tas[plus_petit] = self.tas[plus_petit], self.tas[index]
            index = plus_petit

    def mettre_a_jour(self, produit_id, variation):
        nouvelle_entree = (variation, produit_id)

        if len(self.tas) < self.k:
            self.tas.append(nouvelle_entree)
            self._percoler_vers_le_haut(len(self.tas) - 1)
        elif variation > self.tas[0][0]:
            self.tas[0] = nouvelle_entree
            self._percoler_vers_le_bas(0)

    def get_top_5_hausses(self):
        resultat = sorted(self.tas, key=lambda x: x[0], reverse=True)
        return resultat


class TopKNaif:
    def __init__(self, k=5):
        self.k = k
        self.toutes_variations = []

    def mettre_a_jour(self, produit_id, variation):
        self.toutes_variations.append((variation, produit_id))

    def get_top_5_hausses(self):
        triees = sorted(self.toutes_variations, key=lambda x: x[0], reverse=True)
        return triees[: self.k]

