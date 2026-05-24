// Page d'accueil de Tsenan'tsika qui présente le système et adapte
// dynamiquement les fonctionnalités affichées selon le rôle de
// l'utilisateur connecté. Cette adaptation contextuelle garantit
// que chaque utilisateur voit uniquement les fonctionnalités auxquelles
// il a droit, ce qui assure la cohérence avec la barre de navigation
// et le système de protection des routes.

import { Link } from 'react-router-dom';
import { serviceAuth } from '../services/api';

function PageAccueil() {
  // Récupération de l'utilisateur connecté pour adapter l'affichage
  // des fonctionnalités selon son rôle. Cette récupération se fait
  // localement à partir du stockage du navigateur sans appel API.
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  
  // Détermination des fonctionnalités à afficher selon le rôle.
  // Cette logique centralisée garantit que les permissions sont
  // appliquées de manière cohérente avec le reste de l'application.
  const peutVoirTableauBord = utilisateur !== null; 
  
  const peutVoirSaisie = utilisateur && utilisateur.role === 'agent';
  
  const peutVoirItineraire = utilisateur && 
    (utilisateur.role === 'analyste' || utilisateur.role === 'administrateur');

  return (
    <div>
      <div className="carte">
        <h2>Bienvenue sur Tsenan'tsika</h2>
        <p style={{ marginBottom: '1rem' }}>
          Tsenan'tsika est le système national de surveillance des prix
          alimentaires à Madagascar. Notre plateforme permet de suivre en
          temps réel l'évolution des prix des produits de première nécessité
          dans les sept grandes villes du pays, d'identifier rapidement les
          anomalies de prix, et d'optimiser les routes d'approvisionnement
          entre régions productrices et zones en pénurie.
        </p>
        <p>
          Le système couvre actuellement sept villes pilotes que sont
          Antananarivo, Toamasina, Antsirabe, Mahajanga, Fianarantsoa,
          Toliara et Antsiranana, et il suit les prix de sept produits
          essentiels à savoir le riz, le maïs, le manioc, le haricot,
          l'huile, le sucre et le sel.
        </p>
      </div>

      <div className="carte">
        <h2>Fonctionnalités disponibles pour vous</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
          
          {/* Affichage conditionnel du tableau de bord selon le rôle. */}
          {peutVoirTableauBord && (
            <div style={{ padding: '1rem', backgroundColor: '#e8f5e9', borderRadius: '4px' }}>
              <h3 style={{ color: '#2e7d32', marginBottom: '0.5rem' }}>
                Tableau de bord
              </h3>
              <p style={{ marginBottom: '1rem' }}>
                Consultez en temps réel les alertes de prix anormaux et le
                classement des produits avec les plus fortes hausses.
              </p>
              <Link to="/tableau-bord" className="bouton" style={{ textDecoration: 'none', display: 'inline-block' }}>
                Accéder au tableau de bord
              </Link>
            </div>
          )}

          {/* Affichage conditionnel de la saisie de prix selon le rôle. */}
          {peutVoirSaisie && (
            <div style={{ padding: '1rem', backgroundColor: '#fff8e1', borderRadius: '4px' }}>
              <h3 style={{ color: '#e65100', marginBottom: '0.5rem' }}>
                Saisie de prix
              </h3>
              <p style={{ marginBottom: '1rem' }}>
                Espace réservé aux agents de collecte pour soumettre les prix
                observés sur les marchés locaux.
              </p>
              <Link to="/saisie" className="bouton" style={{ textDecoration: 'none', display: 'inline-block' }}>
                Saisir un prix
              </Link>
            </div>
          )}

          {/* Affichage conditionnel du calcul d'itinéraire selon le rôle. */}
          {peutVoirItineraire && (
            <div style={{ padding: '1rem', backgroundColor: '#e1f5fe', borderRadius: '4px' }}>
              <h3 style={{ color: '#01579b', marginBottom: '0.5rem' }}>
                Itinéraire optimal
              </h3>
              <p style={{ marginBottom: '1rem' }}>
                Calculez la route d'approvisionnement la moins coûteuse entre
                deux villes du réseau malgache.
              </p>
              <Link to="/itineraire" className="bouton" style={{ textDecoration: 'none', display: 'inline-block' }}>
                Calculer un itinéraire
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PageAccueil;