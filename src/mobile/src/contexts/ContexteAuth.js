import React, { createContext, useContext, useState, useEffect } from 'react';
import { serviceAuth } from '../services/api';

const ContexteAuth = createContext({
  utilisateur: null,
  chargement: true,
  connecter: async () => {},
  deconnecter: async () => {},
});

export function FournisseurAuth({ children }) {
  const [utilisateur, setUtilisateur] = useState(null);
  const [chargement, setChargement] = useState(true);

  useEffect(() => {
    const verifierSession = async () => {
      try {
        const utilisateurStocke = await serviceAuth.obtenirUtilisateurConnecte();
        if (utilisateurStocke) {
          setUtilisateur(utilisateurStocke);
        }
      } catch (error) {
        console.error('Erreur lors de la vérification de session:', error);
      } finally {
        setChargement(false);
      }
    };

    verifierSession();
  }, []);

  const connecter = async (email, motDePasse) => {
    const resultat = await serviceAuth.seConnecter(email, motDePasse);
    setUtilisateur(resultat.utilisateur);
    return resultat;
  };

  const deconnecter = async () => {
    await serviceAuth.seDeconnecter();
    setUtilisateur(null);
  };

  return (
    <ContexteAuth.Provider value={{ utilisateur, chargement, connecter, deconnecter }}>
      {children}
    </ContexteAuth.Provider>
  );
}

export function utiliserAuth() {
  return useContext(ContexteAuth);
}