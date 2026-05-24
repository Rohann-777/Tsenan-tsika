// Page du tableau de bord de Tsenan'tsika.
// Cette page consulte l'API backend pour récupérer les alertes actives
// et le classement Top-k des produits avec les plus fortes hausses de prix.
// Elle utilise les hooks useState et useEffect pour gérer le cycle de vie
// des données et offrir une expérience utilisateur fluide avec gestion
// des états de chargement et d'erreur.

import { useState, useEffect } from 'react';
import { serviceTableauBord } from '../services/api';
import { serviceAuth } from '../services/api';

function PageTableauBord() {
  // État pour stocker les données du tableau de bord récupérées depuis l'API.
  // Initialement null car aucune donnée n'est encore disponible.
  const [donnees, setDonnees] = useState(null);
  
  // État pour indiquer si une requête est actuellement en cours.
  // Permet d'afficher un message de chargement à l'utilisateur.
  const [chargement, setChargement] = useState(true);
  
  // État pour stocker un éventuel message d'erreur en cas de problème
  // lors de la communication avec le backend.
  const [erreur, setErreur] = useState(null);

  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();

  // Le hook useEffect s'exécute après le premier rendu du composant.
  // Le tableau vide en deuxième argument signifie que cet effet ne se
  // déclenche qu'une seule fois au chargement initial de la page.
  useEffect(() => {
    // Fonction asynchrone pour récupérer les données du tableau de bord.
    // Elle est définie à l'intérieur du useEffect car useEffect lui même
    // ne peut pas être asynchrone directement.
    const recupererDonnees = async () => {
      try {
        // Appel au service qui interroge l'endpoint /api/alertes/tableau-bord
        const reponse = await serviceTableauBord.obtenirTableauBord();
        setDonnees(reponse);
        setErreur(null);
      } catch (err) {
        // En cas d'erreur, on enregistre le message pour l'afficher
        // à l'utilisateur de manière informative.
        setErreur('Impossible de charger le tableau de bord. Vérifiez que le serveur backend est démarré.');
        console.error('Erreur lors du chargement du tableau de bord:', err);
      } finally {
        // Dans tous les cas, on indique que le chargement est terminé
        // pour cacher le message de chargement.
        setChargement(false);
      }
    };

    recupererDonnees();
  }, []);

  // Fonction utilitaire pour formater une date au format français lisible.
  // Cette fonction transforme une date ISO en chaîne formatée comme
  // par exemple "16 mai 2026 à 16:32".
  const formaterDate = (dateIso) => {
    const date = new Date(dateIso);
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Affichage du message de chargement pendant la récupération des données.
  if (chargement) {
    return (
      <div className="carte">
        <h2>Tableau de bord</h2>
        <div className="message-info">
          Chargement des données en cours, veuillez patienter...
        </div>
      </div>
    );
  }

  // Affichage du message d'erreur en cas de problème.
  if (erreur) {
    return (
      <div className="carte">
        <h2>Tableau de bord</h2>
        <div className="message-erreur">
          {erreur}
        </div>
      </div>
    );
  }

  // Affichage normal des données quand tout s'est bien passé.
  return (
    <div>
      {/* Section d'en-tête avec le compteur d'alertes actives.
          Ce compteur attire immédiatement l'attention sur l'état
          général du système et son niveau d'activité actuel. */}
      <div className="carte">
        <h2>Tableau de bord des alertes</h2>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
          <div>
            <p style={{ fontSize: '0.95rem', color: '#616161' }}>
              Synthèse de l'activité du système sur les 7 derniers jours
            </p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#c62828' }}>
              {donnees.nombre_alertes_actives}
            </div>
            <div style={{ fontSize: '0.9rem', color: '#616161' }}>
              alertes actives
            </div>
          </div>
        </div>
      </div>

      {/* Disposition en deux colonnes pour les alertes et le Top-k.
          Cette mise en page permet à l'utilisateur de voir simultanément
          les deux types d'informations sans avoir à faire défiler la page. */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        
        {/* Section des alertes récentes affichées sous forme de liste détaillée.
            Chaque alerte indique le produit concerné, la ville touchée
            et la date de déclenchement. */}
        <div className="carte">
          <h2>Alertes récentes</h2>
          {donnees.alertes_recentes.length === 0 ? (
            <div className="message-info">
              Aucune alerte active actuellement. Le marché est stable.
            </div>
          ) : (
            <div>
              {donnees.alertes_recentes.map((alerte) => (
                <div key={alerte.id} className="carte carte-alerte" style={{ marginBottom: '0.75rem', padding: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <strong style={{ color: '#c62828', fontSize: '1.1rem' }}>
                        {alerte.produit_nom}
                      </strong>
                      <span style={{ marginLeft: '0.5rem', color: '#616161' }}>
                        à {alerte.ville_nom}
                      </span>
                    </div>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#757575', marginTop: '0.25rem' }}>
                    Déclenchée le {formaterDate(alerte.date)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section du classement Top-k des plus fortes hausses de prix.
            Ce classement est maintenu en temps réel par le tas binaire
            côté backend et reflète les variations les plus significatives
            observées récemment. */}
        <div className="carte">
          <h2>Top 5 des hausses</h2>
          {donnees.top_5_hausses.length === 0 ? (
              <div className="message-info">
                {utilisateur && utilisateur.role === 'agent' ? (
                  <>
                    Aucune variation de prix significative enregistrée pour le moment.
                    Effectuez quelques saisies de prix pour alimenter le classement.
                  </>
                ) : utilisateur && utilisateur.role === 'administrateur' ? (
                  <>
                    Aucune variation de prix significative enregistrée pour le moment.
                    Le classement se remplira automatiquement lorsque les agents 
                    soumettront des prix présentant des écarts notables.
                  </>
                ) : (
                  <>
                    Aucune variation de prix significative n'a été enregistrée récemment.
                    Cette section se mettra à jour automatiquement dès que des écarts 
                    notables seront détectés sur les marchés observés.
                  </>
                )}
              </div>
            ) : (
            <div>
              {donnees.top_5_hausses.map((entree) => (
                <div key={entree.produit_id} className="entree-top-k">
                  <span className="rang">#{entree.rang}</span>
                  <span style={{ flex: 1, marginLeft: '1rem', fontWeight: '500' }}>
                    {entree.produit_nom}
                  </span>
                  <span className="variation">
                    +{entree.variation_pourcent}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Section d'explication pédagogique pour les visiteurs du système.
          Cette section aide les utilisateurs à comprendre ce qu'ils voient
          et comment le système détecte les anomalies de prix. */}
      <div className="carte" style={{ marginTop: '1.5rem' }}>
        <h2>Comment fonctionne le système</h2>
        <p>
          Tsenan'tsika analyse en continu les prix soumis par les agents de
          collecte répartis dans les sept villes pilotes. Quand un nouveau
          prix est saisi, le système calcule automatiquement sa variation
          par rapport à la moyenne récente du produit dans la même ville.
          Si cette variation dépasse 20 pour cent, une alerte est immédiatement
          déclenchée pour signaler une anomalie potentielle pouvant indiquer
          une pénurie, une spéculation, ou un événement perturbateur sur le marché.
        </p>
        <p style={{ marginTop: '0.75rem' }}>
          Le classement Top 5 maintient en temps réel les produits ayant connu
          les plus fortes hausses de prix, ce qui permet aux analystes du
          ministère de prioriser leurs interventions sur les situations les
          plus critiques.
        </p>
      </div>
    </div>
  );
}

export default PageTableauBord;