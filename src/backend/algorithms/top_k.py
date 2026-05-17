"""
Module Top-k avec tas binaire (min-heap) pour Tsenan'tsika.

Cet algorithme maintient en temps réel les k éléments les plus
importants d'un flux continu de données, dans notre cas les 5
produits avec la plus forte hausse de prix. L'implémentation utilise
un tas binaire de taille fixe k, ce qui garantit une complexité
de O(log k) par mise à jour, indépendamment du nombre total de
variations de prix traitées par le système.

Le tas binaire est implémenté manuellement comme exigé par le
cahier des charges du projet, sans utiliser le module heapq de
Python qui ferait office de bibliothèque toute faite.

Complexité :
- Insertion d'une variation : O(log k) où k est la taille du top
- Récupération du top k complet : O(k log k)
- Espace mémoire : O(k)
"""


class TopK:
    """
    Implémentation manuelle d'un Top-k basé sur un min-heap.
    
    Cette classe maintient les k variations de prix les plus élevées
    parmi toutes les variations qui lui sont soumises. Elle est utilisée
    par le Service pour alimenter le tableau de bord et le système
    d'alertes de Tsenan'tsika.
    
    Chaque variation est stockée sous forme de tuple contenant la
    valeur de la variation et un identifiant unique du produit concerné.
    Cela permet de différencier deux variations de même valeur mais
    pour des produits différents, et de retrouver facilement les
    informations complètes lors de l'affichage.
    """

    def __init__(self, k=5):
        """
        Initialise le Top-k avec une capacité maximale de k éléments.
        
        Par défaut, k vaut 5 pour correspondre à l'exigence du cahier
        des charges qui demande les 5 produits avec la plus forte
        hausse de prix. La valeur peut être changée pour d'autres
        cas d'usage si nécessaire.
        """
        self.k = k
        self.tas = []

    def _parent(self, index):
        """
        Retourne l'index du parent d'un nœud dans la représentation
        en tableau du tas binaire.
        
        La formule (index - 1) // 2 vient de la structure d'arbre
        binaire stockée linéairement. Pour un nœud à l'index i, ses
        deux enfants sont aux indices 2i+1 et 2i+2, donc son parent
        est nécessairement à l'index (i-1)//2.
        """
        return (index - 1) // 2

    def _enfant_gauche(self, index):
        """
        Retourne l'index de l'enfant gauche d'un nœud.
        """
        return 2 * index + 1

    def _enfant_droit(self, index):
        """
        Retourne l'index de l'enfant droit d'un nœud.
        """
        return 2 * index + 2

    def _percoler_vers_le_haut(self, index):
        """
        Fait remonter un nœud dans le tas tant qu'il viole la propriété
        de min-heap, c'est-à-dire tant qu'il est plus petit que son parent.
        
        Cette opération est utilisée après une insertion à la fin du
        tableau pour replacer le nouvel élément à sa position correcte.
        Elle parcourt au maximum la hauteur du tas, soit O(log k) opérations.
        """
        while index > 0:
            parent = self._parent(index)
            # On compare uniquement la valeur de variation, pas l'identifiant produit
            if self.tas[index][0] < self.tas[parent][0]:
                # Échange du nœud avec son parent
                self.tas[index], self.tas[parent] = self.tas[parent], self.tas[index]
                index = parent
            else:
                # Si le nœud est plus grand ou égal à son parent, la propriété
                # est respectée et on peut arrêter la remontée
                break

    def _percoler_vers_le_bas(self, index):
        """
        Fait descendre un nœud dans le tas tant qu'il viole la propriété
        de min-heap, c'est-à-dire tant qu'il est plus grand que l'un de
        ses enfants.
        
        Cette opération est utilisée après le remplacement de la racine
        pour replacer l'élément à sa position correcte. À chaque étape,
        on échange le nœud avec le plus petit de ses deux enfants.
        Comme pour la percolation vers le haut, cette opération est en O(log k).
        """
        n = len(self.tas)
        while True:
            gauche = self._enfant_gauche(index)
            droit = self._enfant_droit(index)
            plus_petit = index

            # On cherche le plus petit parmi le nœud courant et ses enfants
            if gauche < n and self.tas[gauche][0] < self.tas[plus_petit][0]:
                plus_petit = gauche
            if droit < n and self.tas[droit][0] < self.tas[plus_petit][0]:
                plus_petit = droit

            # Si le nœud courant est déjà le plus petit, la propriété est respectée
            if plus_petit == index:
                break

            # Sinon on échange avec le plus petit enfant et on continue
            self.tas[index], self.tas[plus_petit] = self.tas[plus_petit], self.tas[index]
            index = plus_petit

    def mettre_a_jour(self, produit_id, variation):
        """
        Insère une nouvelle variation de prix dans le Top-k.
        
        Cette méthode correspond à celle définie dans le diagramme
        de classes. Elle est appelée par le Service à chaque insertion
        d'un nouveau prix validé, pour maintenir en temps réel le
        classement des plus fortes hausses.
        
        La logique est la suivante. Si le tas n'est pas encore plein,
        on ajoute simplement la nouvelle variation et on la fait
        remonter à sa place. Si le tas est plein, on compare la
        nouvelle variation avec la racine, qui est la plus petite
        des k variations actuellement dans le top. Si la nouvelle
        variation est plus grande, elle mérite d'entrer dans le top
        et on remplace la racine, puis on fait descendre la nouvelle
        racine à sa place. Sinon, la nouvelle variation est trop
        petite et on l'ignore.
        """
        nouvelle_entree = (variation, produit_id)

        if len(self.tas) < self.k:
            # Le tas n'est pas encore plein, on ajoute simplement
            self.tas.append(nouvelle_entree)
            self._percoler_vers_le_haut(len(self.tas) - 1)
        elif variation > self.tas[0][0]:
            # Le tas est plein mais la nouvelle variation mérite d'entrer
            self.tas[0] = nouvelle_entree
            self._percoler_vers_le_bas(0)
        # Si la nouvelle variation est plus petite ou égale à la racine,
        # on ne fait rien car elle ne peut pas faire partie du top k

    def get_top_5_hausses(self):
        """
        Retourne les k variations les plus élevées triées par ordre
        décroissant de variation.
        
        Cette méthode correspond à celle définie dans le diagramme
        de classes. Elle est appelée par le Service quand le tableau
        de bord ou le système d'alertes a besoin du classement actuel.
        
        Le tas binaire ne garantit pas un ordre total, seulement que
        la racine est le minimum. Pour retourner les éléments triés,
        on fait une copie du tas et on en extrait les éléments dans
        l'ordre, ce qui revient à un tri par tas en O(k log k).
        """
        # On trie la liste résultante par ordre décroissant de variation
        # On utilise une copie pour ne pas modifier le tas interne
        resultat = sorted(self.tas, key=lambda x: x[0], reverse=True)
        return resultat


class TopKNaif:
    """
    Solution naïve pour la maintenance des k éléments les plus grands.
    
    Cette implémentation stocke toutes les variations dans une liste
    classique et trie cette liste à chaque demande du top k. Elle
    sert de baseline pour mesurer le gain de performance apporté
    par l'approche avec tas binaire.
    
    Complexité :
    - Insertion d'une variation : O(1)
    - Récupération du top k : O(n log n) où n est le nombre total
      de variations stockées
    """

    def __init__(self, k=5):
        """
        Initialise la solution naïve avec une capacité de top k.
        Toutes les variations soumises sont stockées sans optimisation.
        """
        self.k = k
        self.toutes_variations = []

    def mettre_a_jour(self, produit_id, variation):
        """
        Ajoute simplement la nouvelle variation à la liste sans aucune
        comparaison ni tri. Cette approche est en temps constant mais
        elle stocke toutes les données, ce qui devient coûteux en
        mémoire et lent à interroger.
        """
        self.toutes_variations.append((variation, produit_id))

    def get_top_5_hausses(self):
        """
        Trie toute la liste des variations par ordre décroissant et
        retourne les k premiers éléments. Cette opération est lente
        car elle doit retrier l'ensemble des données à chaque appel.
        """
        triees = sorted(self.toutes_variations, key=lambda x: x[0], reverse=True)
        return triees[: self.k]