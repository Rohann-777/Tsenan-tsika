# Fiche récapitulative des algorithmes — Tsenan'tsika

## Vue d'ensemble du projet

Tsenan'tsika intègre quatre algorithmes avancés appartenant à quatre familles différentes, conformément aux exigences du projet transversal L2 qui demande au minimum deux familles d'algorithmes avancés. Le projet utilise également cinq structures de données avancées qui dépassent largement l'exigence minimale de trois structures. Chaque algorithme répond à un besoin métier précis du système de surveillance des prix alimentaires et a été implémenté manuellement sans utilisation de bibliothèque externe, conformément aux exigences académiques.

Les quatre algorithmes sont Rabin-Karp pour la détection de doublons dans la famille Chaînes et Recherche, Fenwick Tree pour le calcul de moyennes sur intervalles dans la famille Optimisation, Top-k avec tas binaire pour la détection des hausses anormales dans la famille Streaming et Fenêtrage, et Dijkstra pour le calcul d'itinéraires optimaux dans la famille Graphes et Réseaux.

---

## Algorithme 1 — Rabin-Karp

### Définition du problème

Quand un agent de collecte saisit un nouveau prix dans le système Tsenan'tsika, le système doit vérifier rapidement si ce rapport n'est pas un doublon d'un rapport déjà soumis dans les dernières vingt-quatre heures. Un doublon peut être soit une erreur involontaire de l'agent qui soumet deux fois la même information, soit une tentative volontaire de manipulation des données. Le problème consiste donc à comparer efficacement la chaîne caractéristique du nouveau rapport avec celles de tous les rapports récents stockés en base, sans dégrader les performances du système quand le volume de données augmente.

Les entrées de l'algorithme sont la chaîne normalisée du nouveau rapport construite à partir du produit, de la ville, du prix et de la date arrondie à l'heure, ainsi que la liste des hachages précalculés des rapports existants accompagnés de leurs chaînes originales. La sortie de l'algorithme est une valeur booléenne indiquant si un doublon a été détecté.

### Modèle utilisé

L'algorithme repose sur le hachage polynomial, une technique qui transforme une chaîne de caractères en un nombre unique en traitant la chaîne comme un nombre écrit dans une certaine base. Pour une chaîne de longueur n composée des caractères c0 à c(n-1), le hachage est calculé selon la formule suivante. Le hachage égale c zéro multiplié par la base à la puissance n moins un, plus c un multiplié par la base à la puissance n moins deux, et ainsi de suite jusqu'à c n moins un multiplié par la base à la puissance zéro, le tout modulo un nombre premier choisi.

Dans notre implémentation, la base utilisée est deux cent cinquante-six pour couvrir tous les caractères ASCII étendus, et le modulo est cent un qui est un nombre premier suffisamment petit pour des calculs rapides tout en limitant les collisions.

### Pseudo-code
fonction calculer_hachage(chaine):
hachage = 0
pour chaque caractere dans chaine:
hachage = (hachage * base + valeur_ascii(caractere)) modulo modulo
retourner hachage
fonction verifier_doublon(nouveau_rapport, rapports_existants):
chaine_nouveau = normaliser(nouveau_rapport)
hachage_nouveau = calculer_hachage(chaine_nouveau)
pour chaque (hachage_existant, chaine_existante) dans rapports_existants:
    si hachage_nouveau == hachage_existant:
        si chaine_nouveau == chaine_existante:
            retourner vrai

retourner faux

### Structures de données utilisées

La structure principale associée à cet algorithme est l'empreinte de hachage. Les empreintes des rapports existants sont précalculées et conservées avec leurs chaînes originales, ce qui permet de remplacer une comparaison de chaînes par une comparaison de nombres entiers, bien plus rapide. Le principe relève de la famille des tables de hachage ; dans le prototype, le cache des empreintes est maintenu sous forme d'une liste de couples empreinte-chaîne, une mise en cache en base de données avec indexation par hachage constituant l'évolution naturelle pour un déploiement à grande échelle.

### Analyse de complexité

La fonction calculer_hachage parcourt chaque caractère de la chaîne exactement une fois en effectuant des opérations en temps constant, ce qui donne une complexité de O(m) où m est la longueur de la chaîne. La fonction verifier_doublon parcourt les n rapports existants et effectue une comparaison de hachage en temps constant pour chacun. Quand un hachage correspond, ce qui est rare grâce au choix d'un nombre premier comme modulo, on effectue une comparaison caractère par caractère en O(m). La complexité totale est donc de O(m+n), où n est le nombre de rapports comparés et m la longueur moyenne d'une chaîne.

En comparaison, la solution naïve qui compare directement les chaînes sans hachage préalable a une complexité de O(n*m), car chaque comparaison de chaînes prend un temps proportionnel à leur longueur. Le gain théorique de Rabin-Karp avec hachages précalculés est donc significatif quand n et m sont grands.

### Tests et validation

L'algorithme a été validé par six tests unitaires couvrant la détection correcte de doublons identiques, l'acceptation de rapports uniques, la normalisation correcte de la casse et des espaces, la distinction de prix différents pour le même produit, la cohérence des résultats entre la version optimisée et la version naïve, et la mesure de performance comparative entre les deux versions.

### Résultats expérimentaux

Sur un jeu de données de deux mille rapports existants avec deux mille vérifications successives, la mesure étant moyennée sur cinq exécutions pour fiabiliser le résultat, les performances comparées sont les suivantes. La solution naïve compare directement les chaînes à chaque vérification, en reparcourant toute la liste des rapports existants. La solution Rabin-Karp précalcule une seule fois les empreintes de hachage des rapports existants, puis chaque vérification se réduit à des comparaisons de nombres entiers. Le gain de performance mesuré est de 76,9 fois plus rapide en faveur de Rabin-Karp. Ce résultat illustre un point essentiel : Rabin-Karp n'est avantageux que lorsque le coût du calcul des empreintes est amorti sur de nombreuses vérifications, ce qui correspond exactement au cas réel où de multiples agents soumettent des prix tout au long de la journée contre une base de rapports déjà hachés.

---

## Algorithme 2 — Fenwick Tree

### Définition du problème

Le tableau de bord de Tsenan'tsika doit afficher en temps réel les moyennes mobiles des prix sur différentes périodes glissantes, par exemple la moyenne du prix du riz à Antananarivo sur les sept derniers jours ou les trente derniers jours. Ces calculs doivent être rapides même quand le volume de données accumulées est important, et la structure doit pouvoir être mise à jour efficacement chaque fois qu'un nouveau prix est saisi par un agent.

Les entrées de l'algorithme sont une liste de prix indexés par date et un intervalle défini par une date de début et une date de fin. La sortie de l'algorithme est la moyenne des prix sur l'intervalle demandé.

### Modèle utilisé

Le Fenwick Tree, aussi appelé Binary Indexed Tree, est une structure de données qui stocke des sommes partielles à des positions stratégiques déterminées par la représentation binaire des indices. Chaque case du tableau interne stocke la somme d'un certain nombre d'éléments précédents, ce nombre étant égal à la valeur du bit le moins significatif de l'index de la case en représentation binaire.

Cette organisation permet de naviguer dans la structure en utilisant des manipulations binaires simples. Pour calculer une somme préfixe, on parcourt les cases en retirant le bit le moins significatif à chaque étape. Pour mettre à jour une valeur, on parcourt les cases en ajoutant le bit le moins significatif à chaque étape.

### Pseudo-code
classe FenwickTree:
fonction __init__(taille):
    arbre = tableau de zeros de longueur taille + 1

fonction mettre_a_jour(index, valeur):
    i = index + 1
    tant que i <= taille:
        arbre[i] = arbre[i] + valeur
        i = i + (i ET -i)

fonction somme_prefixe(index):
    i = index + 1
    somme = 0
    tant que i > 0:
        somme = somme + arbre[i]
        i = i - (i ET -i)
    retourner somme

fonction somme_intervalle(debut, fin):
    si debut == 0:
        retourner somme_prefixe(fin)
    retourner somme_prefixe(fin) - somme_prefixe(debut - 1)

fonction calculer_moyenne(debut, fin):
    somme = somme_intervalle(debut, fin)
    nombre_elements = fin - debut + 1
    retourner somme / nombre_elements

### Structures de données utilisées

La structure principale est évidemment le Fenwick Tree lui-même, qui est une variante des arbres de segments faisant partie des structures avancées requises par le projet. Le Fenwick Tree utilise un simple tableau en interne mais l'organisation des sommes partielles permet d'obtenir les propriétés d'un arbre sans en payer le coût mémoire.

### Analyse de complexité

L'opération de mise à jour parcourt au maximum la hauteur de l'arbre implicite, qui est de l'ordre du logarithme du nombre d'éléments. La complexité d'une mise à jour est donc de O(log n). Le calcul d'une somme préfixe suit le même raisonnement et a également une complexité de O(log n). Le calcul d'une somme d'intervalle effectue deux calculs de somme préfixe, ce qui maintient la complexité à O(log n).

En comparaison, la solution naïve avec un simple tableau a une complexité de O(1) pour les mises à jour mais une complexité de O(n) pour les calculs de somme d'intervalle car il faut parcourir tous les éléments concernés. Le Fenwick Tree offre donc un excellent compromis quand les deux types d'opérations sont fréquents, ce qui est le cas dans Tsenan'tsika.

### Tests et validation

L'algorithme a été validé par cinq tests unitaires couvrant le calcul correct de sommes simples, le calcul correct de moyennes sur une période hebdomadaire de prix, le cumul correct de mises à jour multiples sur le même index, la cohérence des résultats entre la version optimisée et la version naïve, et la mesure de performance comparative.

### Résultats expérimentaux

Sur un jeu de données de vingt mille éléments avec cinq mille requêtes de somme d'intervalle, la mesure étant moyennée sur cinq exécutions, les performances comparées sont les suivantes. La solution naïve recalcule chaque somme d'intervalle par parcours linéaire des éléments concernés. La solution Fenwick Tree répond à chaque requête en temps logarithmique grâce à ses sommes partielles. Le gain de performance mesuré est de 38,2 fois plus rapide en faveur du Fenwick Tree, et cet écart se creuse encore davantage à mesure que le volume de données et le nombre de requêtes augmentent.

---

## Algorithme 3 — Top-k avec tas binaire

### Définition du problème

Le système Tsenan'tsika doit maintenir en permanence le classement des cinq produits avec la plus forte hausse de prix, parmi toutes les variations de prix soumises par les agents à travers les sept villes pilotes. Ce classement doit pouvoir être consulté instantanément par les analystes et les citoyens via le tableau de bord, et il doit être mis à jour rapidement à chaque nouvelle saisie de prix sans que le système n'ait à retrier l'intégralité des données historiques à chaque consultation.

Les entrées de l'algorithme sont les variations de prix qui arrivent en continu sous forme de tuples associant un identifiant de produit à une valeur de variation. La sortie est la liste des k variations les plus élevées triées par ordre décroissant.

### Modèle utilisé

L'algorithme utilise un min-heap, ou tas binaire minimum, comme structure de données principale. Contrairement à l'intuition qui suggérerait d'utiliser un max-heap pour maintenir les plus grandes valeurs, le min-heap est en réalité le bon choix car il permet d'accéder rapidement à la plus petite des k valeurs actuellement dans le top, qui est précisément le seuil à dépasser pour qu'une nouvelle variation mérite d'entrer dans le classement.

Le tas binaire est implémenté comme un arbre binaire stocké linéairement dans un tableau. Pour un nœud à l'index i dans le tableau, son enfant gauche se trouve à l'index deux fois i plus un, son enfant droit à l'index deux fois i plus deux, et son parent à l'index i moins un divisé par deux en division entière. La propriété fondamentale du min-heap est que chaque nœud parent est inférieur ou égal à ses deux enfants, ce qui garantit que la racine du tas est toujours la plus petite valeur.

### Pseudo-code
classe TopK:
fonction __init__(k):
    tas = liste vide

fonction mettre_a_jour(produit_id, variation):
    nouvelle_entree = (variation, produit_id)
    
    si longueur(tas) < k:
        tas.ajouter(nouvelle_entree)
        percoler_vers_le_haut(longueur(tas) - 1)
    sinon si variation > tas[0].variation:
        tas[0] = nouvelle_entree
        percoler_vers_le_bas(0)

fonction percoler_vers_le_haut(index):
    tant que index > 0:
        parent = (index - 1) division_entiere 2
        si tas[index].variation < tas[parent].variation:
            echanger tas[index] et tas[parent]
            index = parent
        sinon:
            arreter

fonction percoler_vers_le_bas(index):
    n = longueur(tas)
    tant que vrai:
        gauche = 2 * index + 1
        droit = 2 * index + 2
        plus_petit = index
        
        si gauche < n et tas[gauche].variation < tas[plus_petit].variation:
            plus_petit = gauche
        si droit < n et tas[droit].variation < tas[plus_petit].variation:
            plus_petit = droit
        
        si plus_petit == index:
            arreter
        
        echanger tas[index] et tas[plus_petit]
        index = plus_petit

fonction get_top_5_hausses():
    retourner trier(tas, decroissant)

### Structures de données utilisées

La structure principale est le tas binaire minimum, qui fait partie des structures avancées requises par le projet. Le tas est stocké dans un simple tableau Python, ce qui économise la mémoire qu'utiliseraient des pointeurs explicites entre les nœuds de l'arbre.

### Analyse de complexité

L'insertion d'une nouvelle variation comporte deux cas. Si le tas n'est pas encore plein, on ajoute simplement l'élément à la fin et on le fait remonter à sa place, ce qui prend au maximum la hauteur du tas, soit O(log k). Si le tas est plein, on compare avec la racine en temps constant, puis selon le résultat on remplace la racine et on fait descendre le nouvel élément, ce qui prend également O(log k). Comme k est fixé à cinq dans notre cas, le logarithme de k est essentiellement une constante très petite, ce qui rend cette opération pratiquement en temps constant.

La récupération du top k complet trie une copie du tas en O k(log k). Avec k égal à cinq, c'est également très rapide.

En comparaison, la solution naïve stocke toutes les variations et les trie à chaque consultation, avec une complexité de O n(log n) par consultation où n est le nombre total de variations accumulées. Quand n devient grand, la solution naïve devient prohibitive.

### Tests et validation

L'algorithme a été validé par six tests unitaires couvrant le remplissage initial correct du tas, le remplacement de la plus petite valeur quand une plus grande arrive, l'ignorance correcte des valeurs trop petites, le tri décroissant des résultats, la cohérence avec la solution naïve, et la mesure de performance comparative.

### Résultats expérimentaux

Sur un flux de cinquante mille variations avec consultation du top cinq, la mesure étant moyennée sur cinq exécutions, les performances comparées sont les suivantes. La solution naïve conserve toutes les variations et les trie pour extraire les cinq plus fortes. La solution avec tas binaire maintient en permanence les cinq plus fortes hausses en temps logarithmique par insertion. Le gain de performance mesuré est de 3,7 fois plus rapide en faveur du tas binaire. Ce gain est plus modéré que pour Rabin-Karp ou le Fenwick Tree, car la solution naïve de référence reste relativement légère : maintenir seulement cinq éléments ne représente pas un coût considérable au départ. L'avantage du tas binaire devient néanmoins déterminant lorsque le nombre d'insertions devient très grand.

---

## Algorithme 4 — Dijkstra

### Définition du problème

Quand un analyste du ministère identifie une ville en pénurie d'un produit alimentaire, il interroge le système Tsenan'tsika pour connaître la route d'approvisionnement la moins coûteuse depuis une autre ville. Le réseau routier malgache est modélisé comme un graphe pondéré où les sommets sont les villes et les arêtes sont les routes directes entre villes, avec des coûts de transport calculés comme la distance multipliée par un indice carburant.

Les entrées de l'algorithme sont le graphe routier sous forme de liste d'adjacence, la ville de départ et la ville de destination. La sortie est le chemin optimal sous forme de liste de villes traversées, accompagné du coût total et d'un indicateur d'atteignabilité.

### Modèle utilisé

L'algorithme de Dijkstra repose sur le principe d'optimalité de Bellman qui stipule que tout sous-chemin d'un chemin optimal est lui-même optimal. À chaque étape, l'algorithme sélectionne le sommet non visité ayant la plus petite distance estimée depuis le sommet de départ et marque cette distance comme définitive. Cette garantie d'optimalité repose sur le fait que tous les poids des arêtes sont strictement positifs, ce qui rend impossible qu'un détour par un sommet ayant une distance estimée plus grande puisse aboutir à un meilleur résultat.

L'efficacité de l'algorithme dépend de la structure de données utilisée pour stocker les sommets non visités et trouver rapidement celui de distance minimale. Notre implémentation utilise un tas binaire minimum comme file de priorité, ce qui réduit la complexité de recherche du minimum de O(V) à O(log V).

### Pseudo-code
fonction calculer_chemin_optimal(graphe, depart, arrivee):
distances = dictionnaire avec infini pour tous les sommets
distances[depart] = 0
predecesseurs = dictionnaire avec nul pour tous les sommets
visites = ensemble vide
file = min_heap contenant (0, depart)
tant que file n'est pas vide:
    (distance_courante, sommet) = extraire_minimum(file)
    
    si sommet dans visites:
        continuer
    
    visites.ajouter(sommet)
    
    si sommet == arrivee:
        arreter
    
    pour chaque (voisin, cout) dans graphe[sommet]:
        si voisin pas dans visites:
            nouvelle_distance = distance_courante + cout
            si nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                predecesseurs[voisin] = sommet
                inserer(file, (nouvelle_distance, voisin))

chemin = reconstruire_chemin(predecesseurs, depart, arrivee)
retourner (chemin, distances[arrivee])

### Structures de données utilisées

L'algorithme utilise plusieurs structures complémentaires. Le graphe est représenté par une liste d'adjacence stockée comme un dictionnaire de listes, ce qui est plus économe en mémoire qu'une matrice d'adjacence pour les graphes peu denses comme le réseau routier malgache. La file de priorité est implémentée comme un tas binaire minimum, ce qui réutilise la structure développée pour le Top-k. Le dictionnaire des prédécesseurs permet de reconstruire le chemin complet à la fin de l'algorithme en remontant depuis l'arrivée jusqu'au départ.

### Analyse de complexité

Chaque sommet est extrait du tas au maximum une fois, ce qui donne O(V) extractions, chacune coûtant O(log V). Pour chaque sommet extrait, on examine tous ses voisins, ce qui donne au total O(E) opérations de relaxation sur l'ensemble de l'exécution. Chaque relaxation peut insérer un nouvel élément dans le tas en grand O du logarithme de V. La complexité totale est donc de grand O de la somme de V et E, multipliée par le logarithme de V.

En comparaison, la solution naïve qui utilise une liste linéaire pour trouver le minimum à chaque étape a une complexité de grand O de V au carré. Pour les graphes denses, les deux complexités sont proches, mais pour les graphes peu denses comme les réseaux routiers réels où E est proche de V, le tas binaire offre un gain significatif.

### Tests et validation

L'algorithme a été validé par six tests unitaires couvrant le calcul correct de chemins directs, le calcul correct de chemins avec escales multiples, le choix correct du chemin optimal quand plusieurs alternatives existent, le cas particulier où départ et arrivée sont identiques, la cohérence avec la solution naïve, et la mesure de performance comparative.

### Résultats expérimentaux

Sur un graphe aléatoire de deux mille sommets avec environ trente mille arêtes, la mesure étant moyennée sur cinq exécutions, les performances comparées sont les suivantes. La solution naïve recherche le sommet de distance minimale par parcours linéaire de tous les sommets non visités à chaque étape. La solution optimisée utilise un tas binaire comme file de priorité pour obtenir ce minimum en temps logarithmique. Le gain de performance mesuré est de 6,0 fois plus rapide en faveur du tas binaire. Ce gain illustre que les deux versions résolvent correctement le problème, mais que l'usage d'une file de priorité efficace fait la différence, d'autant plus nettement que le graphe grandit, puisque l'écart entre la complexité quadratique de la version naïve et la complexité quasi-linéaire de la version optimisée se creuse sur les grands réseaux.

---

## Tableau récapitulatif des complexités

| Algorithme   | Solution naïve         | Solution optimisée     | Gain mesuré   |
|--------------|------------------------|------------------------|---------------|
| Rabin-Karp   | O(n × m)               | O(n + m)               | 76,9 fois     |
| Fenwick Tree | O(n) par requête       | O(log n) par requête   | 38,2 fois     |
| Top-k        | O(n log n) par requête | O(log k) par insertion | 3,7 fois      |
| Dijkstra     | O(V²)                  | O((V + E) log V)       | 6,0 fois      |

Les gains indiqués ont été mesurés sur la machine de développement, chaque mesure étant moyennée sur cinq exécutions pour atténuer les variations ponctuelles. Ces facteurs ne sont pas des constantes absolues : ils dépendent du volume de données, du cas d'usage et de la qualité de la solution naïve de référence. Ils confirment néanmoins, dans tous les cas, la supériorité de la solution optimisée.

---

## Familles d'algorithmes et structures couvertes

Le projet Tsenan'tsika couvre quatre familles d'algorithmes différentes, dépassant largement l'exigence minimale de deux familles imposée par le projet transversal. La famille Chaînes et Recherche est représentée par Rabin-Karp. La famille Optimisation est représentée par Fenwick Tree. La famille Streaming et Fenêtrage est représentée par Top-k. La famille Graphes et Réseaux est représentée par Dijkstra.

Le projet met en œuvre plusieurs structures de données avancées qui dépassent l'exigence minimale de trois structures. Les structures effectivement utilisées dans le prototype sont le graphe en liste d'adjacence, le tas binaire minimum qui sert à la fois de file de priorité pour Dijkstra et de support au Top-k, le Fenwick Tree, et le cache d'empreintes de hachage pour Rabin-Karp. À ces structures s'ajoutent, comme perspectives d'extension cohérentes avec l'architecture, une véritable table de hachage indexée en base pour les empreintes et une structure Union-Find permettant de vérifier la connexité du graphe des villes avant l'exécution de Dijkstra.

---

## Conformité aux exigences du projet

Cette fiche démontre que le projet Tsenan'tsika respecte intégralement les exigences algorithmiques du document du projet transversal L2. Les quatre algorithmes sont implémentés manuellement sans utilisation de bibliothèque externe. Chaque algorithme dispose d'une solution naïve servant de baseline pour la comparaison. Les mesures de performance ont été effectuées sur des jeux de données réalistes et démontrent empiriquement le gain de l'optimisation. Les complexités sont analysées en grand O avec justification mathématique. Les tests unitaires couvrent à la fois la correction et la performance de chaque algorithme.