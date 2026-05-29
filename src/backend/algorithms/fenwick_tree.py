class FenwickTree:
    def __init__(self, taille):
        self.taille = taille
        self.arbre = [0] * (taille + 1)

    def mettre_a_jour(self, index, valeur):
        i = index + 1
        while i <= self.taille:
            self.arbre[i] += valeur
            i += i & -i

    def somme_prefixe(self, index):
        i = index + 1
        somme = 0
        while i > 0:
            somme += self.arbre[i]
            i -= i & -i
        return somme

    def somme_intervalle(self, debut, fin):
        if debut == 0:
            return self.somme_prefixe(fin)
        return self.somme_prefixe(fin) - self.somme_prefixe(debut - 1)

    def calculer_moyenne(self, debut, fin):
        if debut > fin or debut < 0 or fin >= self.taille:
            return 0
        nombre_elements = fin - debut + 1
        somme = self.somme_intervalle(debut, fin)
        return somme / nombre_elements

class TableauNaif:
    def __init__(self, taille):
        self.taille = taille
        self.valeurs = [0] * taille

    def mettre_a_jour(self, index, valeur):
        if 0 <= index < self.taille:
            self.valeurs[index] += valeur

    def somme_intervalle(self, debut, fin):
        if debut < 0 or fin >= self.taille or debut > fin:
            return 0
        somme = 0
        for i in range(debut, fin + 1):
            somme += self.valeurs[i]
        return somme

    def calculer_moyenne(self, debut, fin):
        if debut > fin or debut < 0 or fin >= self.taille:
            return 0
        nombre_elements = fin - debut + 1
        somme = self.somme_intervalle(debut, fin)
        return somme / nombre_elements
