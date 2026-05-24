// Page de calcul d'itinéraire optimal de Tsenan'tsika.
// Cette page permet aux analystes du ministère de calculer la route
// d'approvisionnement la moins coûteuse entre deux villes du réseau
// routier malgache en utilisant l'algorithme de Dijkstra côté backend.

import { useState, useEffect } from 'react';
import { servicePrix, serviceItineraire } from '../services/api';

function PageItineraire() {
  // Liste des villes disponibles dans le système pour alimenter les
  // menus déroulants de sélection du départ et de la destination.
  const [villes, setVilles] = useState([]);
  
  // Identifiants des villes sélectionnées par l'utilisateur dans les
  // menus déroulants. Ces valeurs seront envoyées à l'API lors du calcul.
  const [villeDepartId, setVilleDepartId] = useState('');
  const [villeDestinationId, setVilleDestinationId] = useState('');
  
  // Résultat du calcul d'itinéraire retourné par le backend après
  // exécution de l'algorithme de Dijkstra.
  const [itineraire, setItineraire] = useState(null);
  
  // États pour la gestion du chargement et des erreurs éventuelles.
  const [chargement, setChargement] = useState(true);
  const [calcul, setCalcul] = useState(false);
  const [erreur, setErreur] = useState(null);

  // Chargement initial de la liste des villes au montage du composant.
  // Cette liste est nécessaire pour permettre à l'utilisateur de
  // sélectionner ses villes de départ et de destination.
  useEffect(() => {
    const chargerVilles = async () => {
      try {
        const villesChargees = await servicePrix.listerVilles();
        setVilles(villesChargees);
        setErreur(null);
      } catch (err) {
        setErreur('Impossible de charger la liste des villes. Vérifiez que le serveur backend est démarré.');
        console.error('Erreur lors du chargement des villes:', err);
      } finally {
        setChargement(false);
      }
    };

    chargerVilles();
  }, []);

  // Gestionnaire de soumission qui appelle l'API pour calculer l'itinéraire
  // optimal entre les deux villes sélectionnées. Cette fonction déclenche
  // l'exécution de l'algorithme de Dijkstra côté backend.
  const gererCalcul = async (evenement) => {
    evenement.preventDefault();
    
    // Validation côté client pour s'assurer que les deux villes sont
    // sélectionnées avant d'envoyer la requête.
    if (!villeDepartId || !villeDestinationId) {
      setErreur('Veuillez sélectionner une ville de départ et une ville de destination.');
      return;
    }
    
    // Vérification qu'on ne demande pas un itinéraire d'une ville vers
    // elle-même, ce qui n'aurait pas de sens métier.
    if (villeDepartId === villeDestinationId) {
      setErreur('La ville de départ et la ville de destination doivent être différentes.');
      return;
    }
    
    setCalcul(true);
    setErreur(null);
    setItineraire(null);
    
    try {
      const resultat = await serviceItineraire.calculerItineraire(
        parseInt(villeDepartId),
        parseInt(villeDestinationId)
      );
      setItineraire(resultat);
    } catch (err) {
      // Le backend peut retourner une erreur 404 si aucun chemin n'existe
      // entre les deux villes, ce qui peut arriver si le graphe routier
      // est fragmenté ou si une ville est isolée.
      if (err.response && err.response.status === 404) {
        setErreur('Aucun itinéraire n\'existe entre ces deux villes dans le réseau routier actuel.');
      } else {
        setErreur('Une erreur est survenue lors du calcul de l\'itinéraire.');
      }
      console.error('Erreur de calcul:', err);
    } finally {
      setCalcul(false);
    }
  };

  // Affichage du message de chargement initial pendant la récupération
  // de la liste des villes.
  if (chargement) {
    return (
      <div className="carte">
        <h2>Itinéraire optimal</h2>
        <div className="message-info">
          Chargement de la liste des villes en cours...
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Section d'introduction qui explique le rôle de cette page
          et le contexte d'utilisation pour les analystes. */}
      <div className="carte">
        <h2>Calcul d'itinéraire d'approvisionnement</h2>
        <p>
          Cette interface permet de calculer la route la moins coûteuse pour
          acheminer un produit alimentaire entre deux villes du réseau
          routier malgache. Le système utilise l'algorithme de Dijkstra
          pour trouver le chemin optimal en tenant compte des distances et
          des coûts de transport calculés à partir d'un indice carburant.
          Cette fonctionnalité est principalement destinée aux analystes du
          ministère qui doivent organiser des opérations d'approvisionnement
          vers des zones en pénurie.
        </p>
      </div>

      {/* Formulaire de sélection des villes de départ et de destination. */}
      <div className="carte">
        <h2>Paramètres du calcul</h2>
        
        {erreur && (
          <div className="message-erreur">
            {erreur}
          </div>
        )}
        
        <form onSubmit={gererCalcul}>
          
          <div className="champ-formulaire">
            <label htmlFor="depart">Ville de départ (productrice)</label>
            <select
              id="depart"
              value={villeDepartId}
              onChange={(e) => setVilleDepartId(e.target.value)}
              disabled={calcul}
            >
              <option value="">-- Sélectionner la ville de départ --</option>
              {villes.map((ville) => (
                <option key={ville.id} value={ville.id}>
                  {ville.nom} ({ville.region})
                </option>
              ))}
            </select>
          </div>

          <div className="champ-formulaire">
            <label htmlFor="destination">Ville de destination (en pénurie)</label>
            <select
              id="destination"
              value={villeDestinationId}
              onChange={(e) => setVilleDestinationId(e.target.value)}
              disabled={calcul}
            >
              <option value="">-- Sélectionner la ville de destination --</option>
              {villes.map((ville) => (
                <option key={ville.id} value={ville.id}>
                  {ville.nom} ({ville.region})
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="bouton" disabled={calcul}>
            {calcul ? 'Calcul en cours...' : 'Calculer l\'itinéraire optimal'}
          </button>
          
        </form>
      </div>

      {/* Affichage du résultat du calcul avec visualisation graphique
          du chemin trouvé par l'algorithme de Dijkstra. */}
      {itineraire && itineraire.atteignable && (
        <div className="carte">
          <h2>Itinéraire optimal trouvé</h2>
          
          <div className="message-succes">
            <strong>Chemin calculé avec succès</strong>
            <p style={{ marginTop: '0.5rem' }}>
              L'algorithme de Dijkstra a trouvé un chemin optimal passant par {itineraire.nombre_etapes} ville{itineraire.nombre_etapes > 1 ? 's' : ''}.
            </p>
          </div>
          
          {/* Visualisation graphique du chemin avec des flèches entre
              les villes pour matérialiser la séquence du trajet. */}
          <div style={{ marginTop: '1.5rem', padding: '1.5rem', backgroundColor: '#f5f5f0', borderRadius: '4px' }}>
            <h3 style={{ marginBottom: '1rem', color: '#2e7d32' }}>
              Chemin recommandé
            </h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '0.5rem' }}>
              {itineraire.chemin.map((etape, index) => (
                <div key={etape.ville_id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{
                    padding: '0.75rem 1.25rem',
                    backgroundColor: index === 0 ? '#c8e6c9' : index === itineraire.chemin.length - 1 ? '#ffcdd2' : '#fff8e1',
                    borderRadius: '4px',
                    border: '1px solid',
                    borderColor: index === 0 ? '#2e7d32' : index === itineraire.chemin.length - 1 ? '#c62828' : '#e65100',
                    fontWeight: '500'
                  }}>
                    <div style={{ fontWeight: 'bold' }}>{etape.nom}</div>
                    <div style={{ fontSize: '0.85rem', color: '#616161' }}>{etape.region}</div>
                  </div>
                  {index < itineraire.chemin.length - 1 && (
                    <span style={{ fontSize: '1.5rem', color: '#2e7d32' }}>→</span>
                  )}
                </div>
              ))}
            </div>
          </div>
          
          {/* Tableau récapitulatif des informations principales de l'itinéraire. */}
          <div style={{ marginTop: '1.5rem' }}>
            <table className="tableau-donnees">
              <tbody>
                <tr>
                  <td><strong>Coût total du trajet</strong></td>
                  <td>{itineraire.cout_total} unités de transport</td>
                </tr>
                <tr>
                  <td><strong>Nombre d'étapes</strong></td>
                  <td>{itineraire.nombre_etapes} ville{itineraire.nombre_etapes > 1 ? 's' : ''}</td>
                </tr>
                <tr>
                  <td><strong>Point de départ</strong></td>
                  <td>{itineraire.chemin[0].nom}</td>
                </tr>
                <tr>
                  <td><strong>Point d'arrivée</strong></td>
                  <td>{itineraire.chemin[itineraire.chemin.length - 1].nom}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          {/* Section explicative sur le fonctionnement de l'algorithme
              pour rendre transparente la méthode de calcul utilisée. */}
          <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#e1f5fe', borderRadius: '4px' }}>
            <h3 style={{ marginBottom: '0.5rem', color: '#01579b' }}>
              À propos de ce calcul
            </h3>
            <p style={{ fontSize: '0.95rem' }}>
              Cet itinéraire a été calculé par l'algorithme de Dijkstra qui
              garantit mathématiquement que le chemin trouvé est le moins
              coûteux parmi tous les chemins possibles. L'algorithme a exploré
              le graphe routier en partant de la ville de départ et a
              progressivement déterminé les distances optimales vers toutes
              les villes accessibles, en s'appuyant sur le principe d'optimalité
              de Bellman qui assure que tout sous-chemin d'un chemin optimal
              est lui-même optimal.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default PageItineraire;