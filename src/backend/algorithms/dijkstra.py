class Dijkstra:
    def __init__(self):
        pass

    def _parent_index(self, index):
        return (index - 1) // 2

    def _enfant_gauche_index(self, index):
        return 2 * index + 1

    def _enfant_droit_index(self, index):
        return 2 * index + 2

    def _percoler_vers_le_haut(self, tas, index):
        while index > 0:
            parent = self._parent_index(index)
            if tas[index][0] < tas[parent][0]:
                tas[index], tas[parent] = tas[parent], tas[index]
                index = parent
            else:
                break

    def _percoler_vers_le_bas(self, tas, index):
        n = len(tas)
        while True:
            gauche = self._enfant_gauche_index(index)
            droit = self._enfant_droit_index(index)
            plus_petit = index

            if gauche < n and tas[gauche][0] < tas[plus_petit][0]:
                plus_petit = gauche
            if droit < n and tas[droit][0] < tas[plus_petit][0]:
                plus_petit = droit

            if plus_petit == index:
                break

            tas[index], tas[plus_petit] = tas[plus_petit], tas[index]
            index = plus_petit

    def _inserer_dans_tas(self, tas, element):
        tas.append(element)
        self._percoler_vers_le_haut(tas, len(tas) - 1)

    def _extraire_minimum(self, tas):
        if not tas:
            return None

        minimum = tas[0]
        if len(tas) == 1:
            tas.pop()
        else:
            tas[0] = tas.pop()
            self._percoler_vers_le_bas(tas, 0)
        return minimum

    def calculer_chemin_optimal(self, graphe, sommet_depart, sommet_arrivee):
        distances = {sommet: float('inf') for sommet in graphe}
        distances[sommet_depart] = 0

        predecesseurs = {sommet: None for sommet in graphe}
        visites = set()

        tas = []
        self._inserer_dans_tas(tas, (0, sommet_depart))

        while tas:
            distance_courante, sommet_courant = self._extraire_minimum(tas)

            if sommet_courant in visites:
                continue

            visites.add(sommet_courant)

            if sommet_courant == sommet_arrivee:
                break

            for voisin, cout_arete in graphe[sommet_courant]:
                if voisin not in visites:
                    nouvelle_distance = distance_courante + cout_arete
                    if nouvelle_distance < distances[voisin]:
                        distances[voisin] = nouvelle_distance
                        predecesseurs[voisin] = sommet_courant
                        self._inserer_dans_tas(tas, (nouvelle_distance, voisin))

        chemin = []
        sommet_actuel = sommet_arrivee

        if distances[sommet_arrivee] == float('inf'):
            return {
                'chemin': [],
                'cout_total': float('inf'),
                'atteignable': False,
            }

        while sommet_actuel is not None:
            chemin.append(sommet_actuel)
            sommet_actuel = predecesseurs[sommet_actuel]

        chemin.reverse()

        return {
            'chemin': chemin,
            'cout_total': distances[sommet_arrivee],
            'atteignable': True,
        }


class DijkstraNaif:
    def calculer_chemin_optimal(self, graphe, sommet_depart, sommet_arrivee):
        distances = {sommet: float('inf') for sommet in graphe}
        distances[sommet_depart] = 0

        predecesseurs = {sommet: None for sommet in graphe}
        visites = set()

        non_visites = list(graphe.keys())

        while non_visites:
            sommet_courant = None
            distance_min = float('inf')

            for sommet in non_visites:
                if distances[sommet] < distance_min:
                    distance_min = distances[sommet]
                    sommet_courant = sommet

            if sommet_courant is None:
                break

            if sommet_courant == sommet_arrivee:
                break

            non_visites.remove(sommet_courant)
            visites.add(sommet_courant)

            for voisin, cout_arete in graphe[sommet_courant]:
                if voisin not in visites:
                    nouvelle_distance = distances[sommet_courant] + cout_arete
                    if nouvelle_distance < distances[voisin]:
                        distances[voisin] = nouvelle_distance
                        predecesseurs[voisin] = sommet_courant

        chemin = []
        sommet_actuel = sommet_arrivee

        if distances[sommet_arrivee] == float('inf'):
            return {
                'chemin': [],
                'cout_total': float('inf'),
                'atteignable': False,
            }

        while sommet_actuel is not None:
            chemin.append(sommet_actuel)
            sommet_actuel = predecesseurs[sommet_actuel]

        chemin.reverse()

        return {
            'chemin': chemin,
            'cout_total': distances[sommet_arrivee],
            'atteignable': True,
        }

