"""
Module Dijkstra pour le calcul d'itinéraires d'approvisionnement
optimaux dans Tsenan'tsika.

Cet algorithme trouve le plus court chemin entre deux villes dans
le graphe routier de Madagascar. Il est utilisé par les analystes
du ministère pour identifier la route la moins coûteuse permettant
d'acheminer un produit depuis une ville productrice vers une ville
en pénurie.

L'implémentation utilise un min-heap pour la file de priorité, ce
qui donne une complexité optimale de O((V + E) log V) où V est le
nombre de villes et E le nombre de connexions routières.

Le min-heap est implémenté manuellement comme exigé par le cahier
des charges qui interdit l'utilisation de bibliothèques toutes
faites pour les algorithmes principaux.
"""


class Dijkstra:
    """
    Implémentation manuelle de l'algorithme de Dijkstra avec file
    de priorité pour le calcul des plus courts chemins dans un graphe
    pondéré à poids positifs.
    
    Le graphe est représenté par une liste d'adjacence, ce qui est
    plus économe en mémoire qu'une matrice d'adjacence pour les
    graphes peu denses comme le réseau routier malgache.
    """

    def __init__(self):
        """
        Initialise l'algorithme. Le graphe sera passé en paramètre
        de la méthode principale, ce qui permet d'utiliser la même
        instance pour différents graphes si nécessaire.
        """
        pass

    def _parent_index(self, index):
        """
        Retourne l'index du parent d'un nœud dans le tas binaire
        utilisé comme file de priorité.
        """
        return (index - 1) // 2

    def _enfant_gauche_index(self, index):
        """
        Retourne l'index de l'enfant gauche d'un nœud dans le tas.
        """
        return 2 * index + 1

    def _enfant_droit_index(self, index):
        """
        Retourne l'index de l'enfant droit d'un nœud dans le tas.
        """
        return 2 * index + 2

    def _percoler_vers_le_haut(self, tas, index):
        """
        Fait remonter un élément dans le tas pour maintenir la
        propriété de min-heap après une insertion.
        
        Chaque élément du tas est un tuple (distance, sommet) où
        on compare uniquement la distance pour ordonner le tas.
        """
        while index > 0:
            parent = self._parent_index(index)
            if tas[index][0] < tas[parent][0]:
                tas[index], tas[parent] = tas[parent], tas[index]
                index = parent
            else:
                break

    def _percoler_vers_le_bas(self, tas, index):
        """
        Fait descendre un élément dans le tas pour maintenir la
        propriété de min-heap après le retrait de la racine.
        """
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
        """
        Insère un nouvel élément dans le tas binaire en le plaçant
        à la fin puis en le faisant remonter à sa place correcte.
        """
        tas.append(element)
        self._percoler_vers_le_haut(tas, len(tas) - 1)

    def _extraire_minimum(self, tas):
        """
        Retire et retourne l'élément avec la plus petite distance
        du tas, qui est toujours la racine.
        
        On remplace la racine par le dernier élément du tas puis on
        fait redescendre cet élément à sa place correcte. Cette
        opération maintient la propriété de min-heap.
        """
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
        """
        Calcule le plus court chemin entre deux sommets dans un graphe
        pondéré à poids positifs.
        
        Cette méthode correspond à celle définie dans le diagramme
        de classes. Elle est appelée par le Service quand un analyste
        demande l'itinéraire d'approvisionnement optimal entre une
        ville productrice et une ville en pénurie.
        
        Le graphe est représenté comme un dictionnaire où chaque clé
        est un sommet et la valeur associée est une liste de tuples
        (voisin, cout) représentant les arêtes sortantes du sommet.
        
        La méthode retourne un dictionnaire contenant le chemin
        optimal et son coût total. Si aucun chemin n'existe entre
        les deux sommets, le coût retourné est infini et le chemin
        est une liste vide.
        """
        # Initialisation des distances. La distance de chaque sommet
        # depuis le sommet de départ est initialisée à l'infini, sauf
        # pour le sommet de départ lui-même qui est à zéro.
        distances = {sommet: float('inf') for sommet in graphe}
        distances[sommet_depart] = 0
        
        # Initialisation des prédécesseurs. On garde trace du sommet
        # précédent dans le plus court chemin pour pouvoir reconstruire
        # le chemin complet à la fin de l'algorithme.
        predecesseurs = {sommet: None for sommet in graphe}
        
        # Ensemble des sommets dont la distance minimale est définitive
        visites = set()
        
        # File de priorité implémentée comme un tas binaire
        # Chaque élément est un tuple (distance, sommet)
        tas = []
        self._inserer_dans_tas(tas, (0, sommet_depart))
        
        while tas:
            # On extrait le sommet non visité avec la plus petite distance
            distance_courante, sommet_courant = self._extraire_minimum(tas)
            
            # Si on a déjà visité ce sommet, on l'ignore.
            # Cela peut arriver car on peut insérer plusieurs fois un même
            # sommet dans le tas avec différentes distances.
            if sommet_courant in visites:
                continue
            
            # On marque le sommet courant comme visité
            visites.add(sommet_courant)
            
            # Optimisation : si on a atteint le sommet d'arrivée, on peut
            # s'arrêter car sa distance est maintenant définitive
            if sommet_courant == sommet_arrivee:
                break
            
            # On examine tous les voisins du sommet courant
            for voisin, cout_arete in graphe[sommet_courant]:
                if voisin not in visites:
                    # On calcule la distance possible en passant par le sommet courant
                    nouvelle_distance = distance_courante + cout_arete
                    
                    # Si cette nouvelle distance est meilleure que l'estimation actuelle
                    # du voisin, on met à jour. C'est l'opération de relaxation.
                    if nouvelle_distance < distances[voisin]:
                        distances[voisin] = nouvelle_distance
                        predecesseurs[voisin] = sommet_courant
                        self._inserer_dans_tas(tas, (nouvelle_distance, voisin))
        
        # Reconstruction du chemin optimal depuis les prédécesseurs
        chemin = []
        sommet_actuel = sommet_arrivee
        
        # Si le sommet d'arrivée n'a pas été atteint, on retourne un résultat vide
        if distances[sommet_arrivee] == float('inf'):
            return {
                'chemin': [],
                'cout_total': float('inf'),
                'atteignable': False
            }
        
        # On remonte le chemin depuis l'arrivée jusqu'au départ
        while sommet_actuel is not None:
            chemin.append(sommet_actuel)
            sommet_actuel = predecesseurs[sommet_actuel]
        
        # On inverse pour avoir le chemin du départ vers l'arrivée
        chemin.reverse()
        
        return {
            'chemin': chemin,
            'cout_total': distances[sommet_arrivee],
            'atteignable': True
        }
class DijkstraNaif:
    """
    Solution naïve de Dijkstra utilisant une liste linéaire au lieu
    d'un tas binaire pour la file de priorité.
    
    À chaque étape, l'algorithme parcourt l'ensemble de la liste
    pour trouver le sommet avec la plus petite distance, ce qui
    coûte O(V) au lieu de O(log V) avec un tas binaire. La complexité
    totale devient O(V²) au lieu de O((V + E) log V).
    
    Cette implémentation sert de baseline pour mesurer le gain de
    performance apporté par l'utilisation du tas binaire dans la
    version optimisée.
    """

    def calculer_chemin_optimal(self, graphe, sommet_depart, sommet_arrivee):
        """
        Calcule le plus court chemin en utilisant une liste linéaire
        comme file de priorité, sans aucune optimisation avancée.
        """
        # Initialisation identique à la version optimisée
        distances = {sommet: float('inf') for sommet in graphe}
        distances[sommet_depart] = 0
        predecesseurs = {sommet: None for sommet in graphe}
        visites = set()
        
        # Liste des sommets non visités
        non_visites = list(graphe.keys())
        
        while non_visites:
            # Recherche linéaire du sommet non visité avec la plus petite distance
            # C'est ici que se trouve la principale différence de complexité
            sommet_courant = None
            distance_min = float('inf')
            for sommet in non_visites:
                if distances[sommet] < distance_min:
                    distance_min = distances[sommet]
                    sommet_courant = sommet
            
            # Si aucun sommet accessible n'est trouvé, on arrête
            if sommet_courant is None:
                break
            
            # Si on a atteint le sommet d'arrivée, on peut s'arrêter
            if sommet_courant == sommet_arrivee:
                break
            
            # On retire le sommet courant de la liste des non visités
            non_visites.remove(sommet_courant)
            visites.add(sommet_courant)
            
            # Relaxation des arêtes sortantes
            for voisin, cout_arete in graphe[sommet_courant]:
                if voisin not in visites:
                    nouvelle_distance = distances[sommet_courant] + cout_arete
                    if nouvelle_distance < distances[voisin]:
                        distances[voisin] = nouvelle_distance
                        predecesseurs[voisin] = sommet_courant
        
        # Reconstruction du chemin
        chemin = []
        sommet_actuel = sommet_arrivee
        
        if distances[sommet_arrivee] == float('inf'):
            return {
                'chemin': [],
                'cout_total': float('inf'),
                'atteignable': False
            }
        
        while sommet_actuel is not None:
            chemin.append(sommet_actuel)
            sommet_actuel = predecesseurs[sommet_actuel]
        
        chemin.reverse()
        
        return {
            'chemin': chemin,
            'cout_total': distances[sommet_arrivee],
            'atteignable': True
        }