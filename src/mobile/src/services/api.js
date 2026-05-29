import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const URL_BACKEND = 'http://172.20.10.3:8000';

const apiClient = axios.create({
  baseURL: URL_BACKEND,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(async (config) => {
  try {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch (error) {
    console.error('Erreur lors de la lecture du token:', error);
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('utilisateur');
    }
    return Promise.reject(error);
  }
);

export const serviceAuth = {
  
  seConnecter: async (email, motDePasse) => {
    // FastAPI attend les credentials au format form-urlencoded pour OAuth2
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', motDePasse);
    
    const reponse = await apiClient.post('/api/auth/connexion', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (reponse.data.access_token) {
      await AsyncStorage.setItem('token', reponse.data.access_token);
      await AsyncStorage.setItem('utilisateur', JSON.stringify(reponse.data.utilisateur));
    }
    
    return reponse.data;
  },
  
  seDeconnecter: async () => {
    await AsyncStorage.removeItem('token');
    await AsyncStorage.removeItem('utilisateur');
  },
  
  obtenirUtilisateurConnecte: async () => {
    try {
      const utilisateurString = await AsyncStorage.getItem('utilisateur');
      if (!utilisateurString) return null;
      return JSON.parse(utilisateurString);
    } catch (error) {
      console.error('Erreur lors de la lecture de l\'utilisateur:', error);
      return null;
    }
  },
  
  estConnecte: async () => {
    const token = await AsyncStorage.getItem('token');
    return token !== null;
  },
};

export const servicePrix = {
  
  listerProduits: async () => {
    const reponse = await apiClient.get('/api/prix/produits');
    return reponse.data;
  },
  
  listerVilles: async () => {
    const reponse = await apiClient.get('/api/prix/villes');
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

export const serviceTableauBord = {
  
  obtenirTableauBord: async () => {
    const reponse = await apiClient.get('/api/alertes/tableau-bord');
    return reponse.data;
  },
};

export default apiClient;