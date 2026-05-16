CREATE TABLE utilisateur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenoms VARCHAR(100) NOT NULL,
    motDePasse VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL
);


CREATE TABLE agent_collecte (
    id INTEGER PRIMARY KEY,
    districtAssigne VARCHAR(100) NOT NULL,
    FOREIGN KEY (id) REFERENCES utilisateur(id)
);

CREATE TABLE produit (
    id SERIAL PRIMARY KEY,
    nomFR VARCHAR(100) NOT NULL,
    nomMG VARCHAR(100) NOT NULL,
    unite VARCHAR(30) NOT NULL,
    categorie VARCHAR(50) NOT NULL
);

CREATE TABLE ville (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL
);

CREATE TABLE connexion_ville (
    id SERIAL PRIMARY KEY,
    villeDepart_id INTEGER NOT NULL,
    villeDestination_id INTEGER NOT NULL,
    cout FLOAT NOT NULL,
    FOREIGN KEY (villeDepart_id) REFERENCES ville(id),
    FOREIGN KEY (villeDestination_id) REFERENCES ville(id)
);

CREATE TABLE rapport_prix (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER NOT NULL,
    ville_id INTEGER NOT NULL,
    prix FLOAT NOT NULL,
    dateHeure TIMESTAMP NOT NULL,
    agent_id INTEGER NOT NULL,
    estDoublon BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (produit_id) REFERENCES produit(id),
    FOREIGN KEY (ville_id) REFERENCES ville(id),
    FOREIGN KEY (agent_id) REFERENCES agent_collecte(id)
);

CREATE TABLE prix_marche (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER NOT NULL,
    ville_id INTEGER NOT NULL,
    prix FLOAT NOT NULL,
    dateSaisie TIMESTAMP NOT NULL,
    agent_id INTEGER NOT NULL,
    FOREIGN KEY (produit_id) REFERENCES produit(id),
    FOREIGN KEY (ville_id) REFERENCES ville(id),
    FOREIGN KEY (agent_id) REFERENCES agent_collecte(id)
);

CREATE TABLE alerte (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER NOT NULL,
    ville_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL,
    FOREIGN KEY (produit_id) REFERENCES produit(id),
    FOREIGN KEY (ville_id) REFERENCES ville(id)
);