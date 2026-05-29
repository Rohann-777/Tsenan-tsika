import axios from 'axios';

const URL_API = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: URL_API,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token_tsenantsika');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (erreur) => {
    return Promise.reject(erreur);
  }
);

apiClient.interceptors.response.use(
  (response) => response,
  (erreur) => {
    if (erreur.response && erreur.response.status === 401) {
      localStorage.removeItem('token_tsenantsika');
      localStorage.removeItem('utilisateur_tsenantsika');
      if (window.location.pathname !== '/connexion' && 
          window.location.pathname !== '/inscription') {
        window.location.href = '/connexion';
      }
    }
    return Promise.reject(erreur);
  }
);

export const serviceAuth = {
  
  seConnecter: async (email, motDePasse) => {
    const donnees = new URLSearchParams();
    donnees.append('username', email);
    donnees.append('password', motDePasse);
    
    const reponse = await axios.post(
      `${URL_API}/api/auth/connexion`,
      donnees,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    
    localStorage.setItem('token_tsenantsika', reponse.data.access_token);
    localStorage.setItem('utilisateur_tsenantsika', JSON.stringify(reponse.data.utilisateur));
    
    return reponse.data;
  },
  
  sInscrire: async (nom, prenoms, email, motDePasse) => {
    const reponse = await apiClient.post('/api/auth/inscription', {
      nom,
      prenoms,
      email,
      mot_de_passe: motDePasse,
    });
    
    localStorage.setItem('token_tsenantsika', reponse.data.access_token);
    localStorage.setItem('utilisateur_tsenantsika', JSON.stringify(reponse.data.utilisateur));
    
    return reponse.data;
  },
  
  seDeconnecter: () => {
    localStorage.removeItem('token_tsenantsika');
    localStorage.removeItem('utilisateur_tsenantsika');
  },
  
  obtenirUtilisateurConnecte: () => {
    const utilisateurJson = localStorage.getItem('utilisateur_tsenantsika');
    return utilisateurJson ? JSON.parse(utilisateurJson) : null;
  },
  
  estConnecte: () => {
    return localStorage.getItem('token_tsenantsika') !== null;
  },
};

// Les autres services restent identiques mais bénéficient maintenant
// de l'authentification automatique via les intercepteurs.
export const servicePrix = {
  listerPrixRecents: async (limite = 100) => {
    const reponse = await apiClient.get(`/api/prix/recents?limite=${limite}`);
    return reponse.data;
  },
  
  listerProduits: async () => {
    const reponse = await apiClient.get('/api/prix/produits');
    return reponse.data;
  },
  
  listerVilles: async () => {
    const reponse = await apiClient.get('/api/prix/villes');
    return reponse.data;
  },
  
  calculerMoyenne: async (produitId, villeId, jours = 7) => {
    const reponse = await apiClient.get(
      `/api/prix/moyenne?produit_id=${produitId}&ville_id=${villeId}&jours=${jours}`
    );
    return reponse.data;
  },
};

export const serviceItineraire = {
  calculerItineraire: async (villeDepartId, villeDestinationId) => {
    const reponse = await apiClient.post('/api/itineraire/calculer', {
      ville_depart_id: villeDepartId,
      ville_destination_id: villeDestinationId,
    });
    return reponse.data;
  },
};

export const serviceSaisie = {
  saisirPrix: async (produitId, villeId, prix, agentId) => {
    const reponse = await apiClient.post('/api/saisie/prix', {
      produit_id: produitId,
      ville_id: villeId,
      prix: prix,
      agent_id: agentId,
    });
    return reponse.data;
  },
};

// Service d'administration qui gère les fonctionnalités réservées
// à l'administrateur du système, à savoir la gestion des utilisateurs
// et la surveillance des rapports doublons détectés par Rabin-Karp.
export const serviceAdmin = {
  
  listerUtilisateurs: async (role = null) => {
    const url = role 
      ? `/api/admin/utilisateurs?role=${role}` 
      : '/api/admin/utilisateurs';
    const reponse = await apiClient.get(url);
    return reponse.data;
  },
  
  creerUtilisateur: async (donnees) => {
    const reponse = await apiClient.post('/api/admin/utilisateurs', donnees);
    return reponse.data;
  },
  
  modifierUtilisateur: async (utilisateurId, modifications) => {
    const reponse = await apiClient.put(
      `/api/admin/utilisateurs/${utilisateurId}`,
      modifications
    );
    return reponse.data;
  },
  
  basculerStatutCompte: async (utilisateurId) => {
    const reponse = await apiClient.patch(
      `/api/admin/utilisateurs/${utilisateurId}/statut`
    );
    return reponse.data;
  },
  
  listerDoublons: async (jours = 30) => {
    const reponse = await apiClient.get(`/api/admin/doublons?jours=${jours}`);
    return reponse.data;
  },
};

export const serviceTableauBord = {
  obtenirTableauBord: async () => {
    const reponse = await apiClient.get('/api/alertes/tableau-bord');
    return reponse.data;
  },
};

export const serviceExport = {
  
  telechargerRapportPdf: async () => {
    const reponse = await apiClient.get('/api/export/rapport-pdf', {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([reponse.data]));
    
    const enteteDisposition = reponse.headers['content-disposition'];
    let nomFichier = 'tsenantsika_rapport.pdf';
    if (enteteDisposition) {
      const correspondance = enteteDisposition.match(/filename="(.+)"/);
      if (correspondance && correspondance[1]) {
        nomFichier = correspondance[1];
      }
    }
    
    const lien = document.createElement('a');
    lien.href = url;
    lien.setAttribute('download', nomFichier);
    document.body.appendChild(lien);
    lien.click();
    
    lien.remove();
    window.URL.revokeObjectURL(url);
  },
};