import { useState, useEffect } from 'react';
import {
  Route, MapPin, ArrowRight, Send, Navigation,
  DollarSign, Layers, Info, Map
} from 'lucide-react';
import { servicePrix, serviceItineraire } from '../services/api';
import '../styles/PageItineraire.css';

function PageItineraire() {
  const [villes, setVilles] = useState([]);
  const [villeDepartId, setVilleDepartId] = useState('');
  const [villeDestinationId, setVilleDestinationId] = useState('');
  const [itineraire, setItineraire] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [calcul, setCalcul] = useState(false);
  const [erreur, setErreur] = useState(null);

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

  const gererCalcul = async (evenement) => {
    evenement.preventDefault();
    
    if (!villeDepartId || !villeDestinationId) {
      setErreur('Veuillez sélectionner une ville de départ et une ville de destination.');
      return;
    }
    
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

  const obtenirTypeEtape = (index, total) => {
    if (index === 0) return 'depart';
    if (index === total - 1) return 'arrivee';
    return 'intermediaire';
  };

  const obtenirLabelEtape = (index, total) => {
    if (index === 0) return 'Départ';
    if (index === total - 1) return 'Arrivée';
    return `Étape ${index}`;
  };

  if (chargement) {
    return (
      <div className="page-itineraire">
        <div className="entete-itineraire">
          <div className="icone-itineraire-grande">
            <Route size={32} />
          </div>
          <div className="contenu-entete-itineraire">
            <h1 className="titre-itineraire">Chargement en cours...</h1>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-itineraire">
      
      {/* En-tête contextuel avec présentation de la fonctionnalité. */}
      <div className="entete-itineraire">
        <div className="icone-itineraire-grande">
          <Route size={32} />
        </div>
        <div className="contenu-entete-itineraire">
          <h1 className="titre-itineraire">Calcul d'itinéraire optimal</h1>
          <p className="description-itineraire">
            Calculez la route d'approvisionnement la moins coûteuse entre 
            deux villes du réseau routier malgache grâce à l'algorithme de Dijkstra.
          </p>
        </div>
      </div>

      {/* Formulaire de sélection des villes avec disposition visuelle. */}
      <div className="carte-formulaire-itineraire">
        <h2 className="titre-formulaire-itineraire">Paramètres du calcul</h2>
        
        {erreur && (
          <div className="message-erreur-auth" style={{ marginBottom: 'var(--espace-md)' }}>
            <span>{erreur}</span>
          </div>
        )}
        
        <form onSubmit={gererCalcul}>
          
          <div className="selection-villes">
            <div className="groupe-champ-moderne">
              <label className="label-champ-moderne">
                Ville de départ
              </label>
              <select
                className="input-itineraire"
                value={villeDepartId}
                onChange={(e) => setVilleDepartId(e.target.value)}
                disabled={calcul}
                required
              >
                <option value="">Sélectionner</option>
                {villes.map((ville) => (
                  <option key={ville.id} value={ville.id}>
                    {ville.nom}
                  </option>
                ))}
              </select>
            </div>

            <div className="fleche-direction">
              <ArrowRight size={20} />
            </div>

            <div className="groupe-champ-moderne">
              <label className="label-champ-moderne">
                Ville de destination
              </label>
              <select
                className="input-itineraire"
                value={villeDestinationId}
                onChange={(e) => setVilleDestinationId(e.target.value)}
                disabled={calcul}
                required
              >
                <option value="">Sélectionner</option>
                {villes.map((ville) => (
                  <option key={ville.id} value={ville.id}>
                    {ville.nom}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button type="submit" className="bouton-calculer" disabled={calcul}>
            {calcul ? (
              <>
                <span className="spinner-saisie"></span>
                Calcul en cours...
              </>
            ) : (
              <>
                <Send size={18} />
                Calculer l'itinéraire optimal
              </>
            )}
          </button>
        </form>
      </div>

      {/* Affichage du résultat avec visualisation graphique du chemin. */}
      {itineraire && itineraire.atteignable && (
        <div className="carte-resultat-itineraire">
          
          <div className="entete-resultat-itineraire">
            <h2 className="titre-resultat-itineraire">
              <Map size={22} color="var(--couleur-tertiaire)" />
              Itinéraire optimal trouvé
            </h2>
            <div className="cout-total-badge">
              <DollarSign size={18} />
              {itineraire.cout_total} unités
            </div>
          </div>

          {/* Visualisation du chemin sous forme de ligne avec étapes. */}
          <div className="chemin-visuel">
            {itineraire.chemin.map((etape, index) => {
              const type = obtenirTypeEtape(index, itineraire.chemin.length);
              const label = obtenirLabelEtape(index, itineraire.chemin.length);
              
              return (
                <div key={etape.ville_id} className="etape-chemin">
                  <div className={`point-etape point-${type}`}>
                    {index + 1}
                  </div>
                  <div className="connecteur-etape"></div>
                  <div className="contenu-etape">
                    <div className="nom-etape">{etape.nom}</div>
                    <div className="region-etape">Région {etape.region}</div>
                    <span className={`badge-etape badge-${type}`}>{label}</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Récapitulatif des informations principales sous forme visuelle. */}
          <div className="recap-itineraire">
            <div className="element-recap">
              <div className="icone-recap">
                <Navigation size={20} />
              </div>
              <div className="contenu-recap">
                <span className="label-recap">Coût total</span>
                <span className="valeur-recap">{itineraire.cout_total}</span>
              </div>
            </div>
            
            <div className="element-recap">
              <div className="icone-recap">
                <Layers size={20} />
              </div>
              <div className="contenu-recap">
                <span className="label-recap">Étapes</span>
                <span className="valeur-recap">{itineraire.nombre_etapes}</span>
              </div>
            </div>
            
            <div className="element-recap">
              <div className="icone-recap">
                <MapPin size={20} />
              </div>
              <div className="contenu-recap">
                <span className="label-recap">Départ</span>
                <span className="valeur-recap">{itineraire.chemin[0].nom}</span>
              </div>
            </div>
            
            <div className="element-recap">
              <div className="icone-recap">
                <MapPin size={20} />
              </div>
              <div className="contenu-recap">
                <span className="label-recap">Arrivée</span>
                <span className="valeur-recap">{itineraire.chemin[itineraire.chemin.length - 1].nom}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Section explicative sur le fonctionnement de Dijkstra. */}
      <div className="section-info-dijkstra">
        <div className="icone-info-dijkstra">
          <Info size={24} />
        </div>
        <div className="contenu-info-dijkstra">
          <div className="titre-info-dijkstra">À propos de l'algorithme de Dijkstra</div>
          <div className="texte-info-dijkstra">
            L'itinéraire calculé garantit mathématiquement le chemin le moins coûteux 
            parmi toutes les routes possibles dans le réseau. L'algorithme explore 
            le graphe en s'appuyant sur le principe d'optimalité de Bellman selon 
            lequel tout sous-chemin d'un chemin optimal est lui-même optimal.
          </div>
        </div>
      </div>
    </div>
  );
}

export default PageItineraire;