"""
Module Fenwick Tree (Binary Indexed Tree) pour Tsenan'tsika.

Cette structure de données permet de calculer rapidement des sommes
sur des intervalles tout en supportant des mises à jour fréquentes.
Elle est utilisée dans le système pour calculer les moyennes mobiles
des prix sur différentes périodes, ce qui alimente le tableau de bord
et le système de détection d'anomalies.

Complexité :
- Mise à jour d'un élément : O(log n)
- Calcul de la somme d'un préfixe : O(log n)
- Calcul de la somme d'un intervalle : O(log n)
- Espace mémoire : O(n)
"""


class FenwickTree:
    """
    Implémentation manuelle d'un Fenwick Tree pour les requêtes
    de somme et de moyenne sur intervalles.
    
    Le Fenwick Tree utilise une structure d'arbre implicite stockée
    dans un tableau. Chaque position du tableau stocke la somme d'un
    certain nombre d'éléments précédents, déterminé par la position
    du bit le moins significatif de son index.
    
    Pour faciliter la manipulation des indices binaires, on utilise
    une indexation à partir de 1 plutôt que 0. La position 0 du tableau
    interne reste inutilisée pour simplifier les calculs.
    """

    def __init__(self, taille):
        """
        Initialise un Fenwick Tree de taille donnée.
        
        Le tableau interne est dimensionné à taille+1 car on utilise
        une indexation à partir de 1. Toutes les positions sont
        initialisées à zéro, ce qui représente un arbre vide.
        """
        self.taille = taille
        self.arbre = [0] * (taille + 1)

    def mettre_a_jour(self, index, valeur):
        """
        Ajoute une valeur à la position donnée dans le Fenwick Tree.
        
        Cette opération met à jour toutes les positions de l'arbre qui
        contiennent l'index donné dans leur intervalle de responsabilité.
        La navigation se fait en ajoutant le bit le moins significatif
        à l'index courant à chaque étape, ce qui correspond à remonter
        vers les positions parentes dans la représentation binaire.
        
        Complexité : O(log n) car on visite au plus log(n) positions.
        """
        # On utilise une indexation à partir de 1 en interne
        i = index + 1
        while i <= self.taille:
            self.arbre[i] += valeur
            # Le bit le moins significatif de i détermine la prochaine position
            i += i & -i

    def somme_prefixe(self, index):
        """
        Calcule la somme des éléments depuis la position 0 jusqu'à
        la position index incluse.
        
        Cette opération combine les sommes partielles stockées aux
        positions stratégiques de l'arbre. La navigation se fait en
        soustrayant le bit le moins significatif à l'index courant
        à chaque étape, ce qui correspond à descendre vers les
        positions ancêtres dans la représentation binaire.
        
        Complexité : O(log n) car on visite au plus log(n) positions.
        """
        # On utilise une indexation à partir de 1 en interne
        i = index + 1
        somme = 0
        while i > 0:
            somme += self.arbre[i]
            # On retire le bit le moins significatif pour aller à la position précédente
            i -= i & -i
        return somme

    def somme_intervalle(self, debut, fin):
        """
        Calcule la somme des éléments entre les positions debut et fin incluses.
        
        Cette méthode exploite une propriété fondamentale des sommes
        préfixes : la somme entre debut et fin égale la somme jusqu'à fin
        moins la somme jusqu'à debut moins un. Cela permet de réutiliser
        directement la méthode somme_prefixe sans calcul supplémentaire.
        
        Complexité : O(log n) car on fait deux appels à somme_prefixe.
        """
        if debut == 0:
            return self.somme_prefixe(fin)
        return self.somme_prefixe(fin) - self.somme_prefixe(debut - 1)

    def calculer_moyenne(self, debut, fin):
        """
        Calcule la moyenne des éléments entre les positions debut et fin incluses.
        
        Cette méthode correspond à celle définie dans le diagramme de classes.
        Elle est utilisée par le service pour fournir des moyennes mobiles
        au tableau de bord et au système de détection d'anomalies.
        
        Note importante : le Fenwick Tree stocke la somme, pas la moyenne.
        On divise donc la somme par le nombre d'éléments dans l'intervalle
        pour obtenir la moyenne. Si l'intervalle est vide ou invalide,
        on retourne zéro pour éviter une division par zéro.
        """
        if debut > fin or debut < 0 or fin >= self.taille:
            return 0
        nombre_elements = fin - debut + 1
        somme = self.somme_intervalle(debut, fin)
        return somme / nombre_elements
class TableauNaif:
    """
    Solution naïve utilisant une simple liste Python pour stocker
    les valeurs et calculer les sommes d'intervalles.
    
    Cette implémentation sert de baseline pour mesurer le gain de
    performance apporté par le Fenwick Tree. Elle représente l'approche
    la plus directe qu'un programmeur débutant utiliserait sans
    connaissance des structures de données avancées.
    
    Complexité :
    - Mise à jour d'un élément : O(1)
    - Calcul de somme d'intervalle : O(n) où n est la taille de l'intervalle
    """

    def __init__(self, taille):
        """
        Initialise un tableau de la taille donnée avec des zéros.
        """
        self.taille = taille
        self.valeurs = [0] * taille

    def mettre_a_jour(self, index, valeur):
        """
        Ajoute une valeur à la position donnée.
        
        Cette opération est en temps constant car on accède directement
        à l'index dans la liste. C'est le seul avantage de cette approche
        par rapport au Fenwick Tree.
        """
        if 0 <= index < self.taille:
            self.valeurs[index] += valeur

    def somme_intervalle(self, debut, fin):
        """
        Calcule la somme des éléments entre les positions debut et fin
        en parcourant l'intervalle élément par élément.
        
        Cette opération est en O(n) car on doit visiter chaque élément
        de l'intervalle. Plus l'intervalle est grand, plus c'est lent.
        """
        if debut < 0 or fin >= self.taille or debut > fin:
            return 0
        somme = 0
        for i in range(debut, fin + 1):
            somme += self.valeurs[i]
        return somme

    def calculer_moyenne(self, debut, fin):
        """
        Calcule la moyenne en parcourant l'intervalle complet.
        
        Comme pour somme_intervalle, cette opération est en O(n).
        """
        if debut > fin or debut < 0 or fin >= self.taille:
            return 0
        nombre_elements = fin - debut + 1
        somme = self.somme_intervalle(debut, fin)
        return somme / nombre_elements