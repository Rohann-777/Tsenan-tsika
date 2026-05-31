# Tsenan'tsika

**Système national de surveillance des prix alimentaires de Madagascar**

Projet transversal L2 — Parcours Services Informatiques aux Organisations — ESMIA Innovation
Année universitaire 2025-2026

---

## Présentation

Tsenan'tsika (« notre marché » en malgache) est un système d'information destiné à surveiller en temps quasi réel les prix des produits alimentaires de première nécessité à Madagascar. Il permet la collecte des prix sur le terrain par des agents affectés à des villes pilotes, la détection automatique des variations anormales, le calcul d'itinéraires d'approvisionnement optimaux, et la consultation d'un tableau de bord par les analystes du ministère et les citoyens.

Le projet repose sur une architecture trois tiers stricte et sur l'implémentation manuelle de quatre algorithmes avancés.

| Algorithme          | Rôle                                           | Complexité             |
|---------------------|------------------------------------------------|------------------------|
| Rabin-Karp          | Détection des saisies dupliquées               | O(n) en moyenne        |
| Fenwick Tree        | Calcul des moyennes mobiles de prix            | O(log n)               |
| Top-k (tas binaire) | Classement des plus fortes hausses             | O(log k) par insertion |
| Dijkstra            | Itinéraire d'approvisionnement de moindre coût | O((V + E) log V)       |

---

## Fonctionnalités

| Code | Fonctionnalité                          | Acteur principal         |
|------|-----------------------------------------|--------------------------|
| F1   | Saisie des prix de marché               | Agent de collecte        |
| F2   | Tableau de bord de surveillance         | Tous les rôles connectés |
| F3   | Calcul d'itinéraire d'approvisionnement | Analyste                 |
| F4   | Surveillance des doublons               | Administrateur           |  
| F5   | Gestion des utilisateurs                | Administrateur           |
| F6   | Export PDF des analyses                 | Analyste                 |

L'application web couvre l'ensemble des fonctionnalités. L'application mobile couvre la saisie des prix (F1) et la consultation du tableau de bord (F2).

---

## Architecture technique

| Composant          | Technologie                  |
|--------------------|------------------------------|
| Backend            | Python 3, FastAPI            |
| Base de données    | PostgreSQL, SQLAlchemy (ORM) |
| Authentification   | JWT, hachage bcrypt          |
| Frontend web       | React (Vite)                 |
| Application mobile | React Native (Expo)          |
| Export PDF         | fpdf2                        |

Le backend suit une architecture en couches : `routes → controllers → services → repositories → base de données`. Les algorithmes sont isolés dans un module dédié.

---

## Prérequis

Avant l'installation, assurez-vous de disposer des outils suivants :

- **Python 3.12 ou supérieur**
- **Node.js 20 ou supérieur** et **npm**
- **PostgreSQL 14 ou supérieur** (serveur local)
- **Git**
- Pour le test mobile : l'application **Expo Go** sur un smartphone iOS ou Android

---

## Installation

### 1. Récupération du projet

```bash
git clone <url-du-depot>
cd Tsenantsika
```

### 2. Configuration de la base de données

Lancez votre serveur PostgreSQL local, puis créez la base de données du projet. Depuis l'outil `psql` ou pgAdmin :

```sql
CREATE DATABASE tsenantsika_db;
```

### 3. Backend

Depuis la racine du projet, créer et activer un environnement virtuel Python, puis installer les dépendances.

```bash
python -m venv venv
```

Activer l'environnement virtuel :

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Installer les dépendances backend :

```bash
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine du projet pour configurer la connexion à la base de données (remplacer `votre_mot_de_passe` par votre mot de passe PostgreSQL) :

```
DATABASE_URL=postgresql://postgres:votre_mot_de_passe@localhost:5432/tsenantsika_db
```

Initialiser les tables, puis peupler la base avec les données de démonstration :

```bash
python -m src.backend.init_db
python -m data.generer_donnees
```

Lancer le serveur backend :

```bash
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

Le backend est accessible sur `http://localhost:8000` et la documentation interactive Swagger sur `http://localhost:8000/docs`.

### 4. Frontend web

Dans un nouveau terminal, depuis le dossier du frontend :

```bash
cd src/frontend
npm install
npm run dev
```

L'application web est accessible à l'adresse indiquée par Vite, généralement `http://localhost:5173`.

### 5. Application mobile

Dans un nouveau terminal, depuis le dossier mobile :

```bash
cd src/mobile
npm install
npx expo start
```

Un QR code s'affiche dans le terminal. Scanner-le avec l'application Expo Go sur votre smartphone.

**Important** : l'ordinateur et le smartphone doivent être sur le même réseau local. L'adresse IP du backend est configurée dans `src/mobile/src/services/api.js` (constante `URL_BACKEND`). Remplacer cette adresse par l'adresse IP locale de votre ordinateur (visible via `ipconfig` sous Windows ou `ifconfig` sous macOS/Linux) et assurez-vous que le backend tourne bien avec l'option `--host 0.0.0.0`.

---

## Comptes de démonstration

| Rôle           | Email                         | Mot de passe |     Ville    |
|----------------|-------------------------------|--------------|--------------|
| Administrateur | admin@tsenantsika.mg          | admin123     |       —      |
| Analyste       | marie.analyste@tsenantsika.mg | analyste123  |       —      |
| Analyste       | paul.analyste@tsenantsika.mg  | analyste123  |       —      |
| Agent          | sophie.agent@tsenantsika.mg   | agent123     | Antananarivo |
| Agent          | pierre.agent@tsenantsika.mg   | agent123     | Toamasina    |
| Agent          | claire.agent@tsenantsika.mg   | agent123     | Fianarantsoa |
| Agent          | hery.agent@tsenantsika.mg     | agent123     | Antsirabe    |
| Agent          | lalaina.agent@tsenantsika.mg  | agent123     | Mahajanga    |
| Agent          | tahiana.agent@tsenantsika.mg  | agent123     | Toliara      |
| Agent          | voahangy.agent@tsenantsika.mg | agent123     | Antsiranana  |
| Citoyen        | tiana.citoyen@tsenantsika.mg  | citoyen123   |        —     |

---

## Structure du projet

```
Tsenantsika/
├── src/
│   ├── backend/
│   │   ├── algorithms/      # Rabin-Karp, Fenwick Tree, Top-k, Dijkstra
│   │   ├── routes/          # Points d'entrée de l'API
│   │   ├── controllers/     # Orchestration des requêtes
│   │   ├── services/        # Logique métier
│   │   ├── repositories/    # Accès aux données
│   │   ├── models/          # Modèles SQLAlchemy
│   │   ├── schemas/         # Schémas Pydantic
│   │   ├── auth/            # Authentification JWT
│   │   ├── config/          # Configuration base de données
│   │   └── main.py          # Point d'entrée FastAPI
│   ├── frontend/            # Application web React (Vite)
│   └── mobile/              # Application mobile React Native (Expo)
├── data/
│   └── generer_donnees.py   # Génération des données de démonstration
├── requirements.txt         # Dépendances Python
└── README.md
```

---

## Tests

Les tests unitaires des algorithmes se lancent depuis la racine du projet avec :

```bash
pytest
```

---

## Notes

- Les algorithmes avancés sont implémentés manuellement, sans bibliothèque externe, conformément aux exigences du projet.
- Le classement Top-k est maintenu en mémoire vive et se réinitialise au redémarrage du serveur ; il se reconstruit au fil des saisies.
- La désactivation d'un compte est une suppression logique qui préserve l'intégrité référentielle et la traçabilité des données.

---

## Auteur

**RAKOTOJAONA Tsiaronomena Rohann** — NIE : SE20240253
Encadré par Monsieur RAZAFINDRAIBE Fabrice