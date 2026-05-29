import { useState, useEffect } from 'react';
import {
  ShieldAlert, AlertTriangle, Search, User, Package,
  MapPin, Calendar, Info, CheckCircle2, Award
} from 'lucide-react';
import { serviceAdmin } from '../services/api';
import '../styles/PageSurveillanceDoublons.css';

function PageSurveillanceDoublons() {
  const [doublons, setDoublons] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);
  const [periodeJours, setPeriodeJours] = useState(30);
  const [recherche, setRecherche] = useState('');

  useEffect(() => {
    chargerDoublons();
  }, [periodeJours]);

  const chargerDoublons = async () => {
    setChargement(true);
    try {
      const donnees = await serviceAdmin.listerDoublons(periodeJours);
      setDoublons(donnees);
      setErreur(null);
    } catch (err) {
      setErreur('Impossible de charger les doublons. Vérifiez que le serveur backend est démarré.');
      console.error(err);
    } finally {
      setChargement(false);
    }
  };

  const doublonsFiltres = doublons.filter(d => {
    if (!recherche) return true;
    const termeRecherche = recherche.toLowerCase();
    return (
      d.agent_nom.toLowerCase().includes(termeRecherche) ||
      d.produit_nom.toLowerCase().includes(termeRecherche) ||
      d.ville_nom.toLowerCase().includes(termeRecherche)
    );
  });

  const statistiquesParAgent = doublons.reduce((acc, d) => {
    if (!acc[d.agent_id]) {
      acc[d.agent_id] = {
        id: d.agent_id,
        nom: d.agent_nom,
        nombre: 0
      };
    }
    acc[d.agent_id].nombre++;
    return acc;
  }, {});

  const agentsAvecPlusDeDoublons = Object.values(statistiquesParAgent)
    .sort((a, b) => b.nombre - a.nombre)
    .slice(0, 3);

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

  if (chargement) {
    return (
      <div className="page-surveillance-doublons">
        <div className="entete-surveillance">
          <div className="contenu-entete-surveillance">
            <div className="icone-surveillance-grande">
              <ShieldAlert size={32} />
            </div>
            <div className="texte-entete-surveillance">
              <h1 className="titre-surveillance">Chargement en cours...</h1>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-surveillance-doublons">
      
      {/* En-tête avec présentation et compteur principal. */}
      <div className="entete-surveillance">
        <div className="contenu-entete-surveillance">
          <div className="icone-surveillance-grande">
            <ShieldAlert size={32} />
          </div>
          <div className="texte-entete-surveillance">
            <h1 className="titre-surveillance">Surveillance des doublons</h1>
            <p className="description-surveillance">
              Consultez les rapports identifiés comme doublons par l'algorithme 
              Rabin-Karp pour analyser les comportements de soumission.
            </p>
          </div>
        </div>
        
        <div className="compteur-doublons-principal">
          <div className="nombre-doublons-grand">{doublons.length}</div>
          <div className="label-doublons-grand">
            Doublons sur {periodeJours} jours
          </div>
        </div>
      </div>

      {/* Section podium des agents avec le plus de doublons. */}
      {agentsAvecPlusDeDoublons.length > 0 && (
        <div className="section-podium-agents">
          <h2 className="titre-podium">
            <Award size={22} color="var(--avertissement)" />
            Agents avec le plus de doublons détectés
          </h2>
          <p className="description-podium">
            Ces agents apparaissent le plus fréquemment dans les doublons détectés. 
            Une présence répétée peut indiquer un problème technique ou un comportement à analyser.
          </p>
          <div className="grille-podium">
            {agentsAvecPlusDeDoublons.map((agent, index) => {
              const rang = index + 1;
              return (
                <div key={agent.id} className={`carte-agent-podium podium-${rang}`}>
                  <div className={`rang-podium rang-${rang}`}>
                    {rang}
                  </div>
                  <div className="contenu-agent-podium">
                    <div className="nom-agent-podium">{agent.nom}</div>
                    <div className="nombre-doublons-agent">
                      {agent.nombre}
                      <span className="label-doublons-agent">
                        doublon{agent.nombre > 1 ? 's' : ''}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Barre de filtrage et recherche. */}
      <div className="barre-filtres-surveillance">
        <div className="conteneur-recherche-doublons">
          <Search size={18} className="icone-recherche-doublons" />
          <input
            type="text"
            className="input-recherche-doublons"
            placeholder="Rechercher par agent, produit ou ville..."
            value={recherche}
            onChange={(e) => setRecherche(e.target.value)}
          />
        </div>
        <select
          className="select-periode"
          value={periodeJours}
          onChange={(e) => setPeriodeJours(parseInt(e.target.value))}
        >
          <option value={7}>7 derniers jours</option>
          <option value={30}>30 derniers jours</option>
          <option value={90}>90 derniers jours</option>
          <option value={365}>1 année</option>
        </select>
      </div>

      {/* Tableau détaillé des doublons ou message d'état vide. */}
      <div className="carte-tableau-doublons">
        {erreur && (
          <div className="message-erreur-modal" style={{ margin: 'var(--espace-md)' }}>
            <AlertTriangle size={18} />
            {erreur}
          </div>
        )}
        
        {doublonsFiltres.length === 0 ? (
          <div className="etat-vide-doublons">
            <div className="icone-etat-vide-doublons">
              <CheckCircle2 size={40} />
            </div>
            <div className="titre-etat-vide-doublons">
              {recherche ? 'Aucun résultat' : 'Système sain'}
            </div>
            <div className="description-etat-vide-doublons">
              {recherche 
                ? 'Aucun doublon ne correspond aux critères de recherche. Essayez d\'élargir la période ou de modifier les termes de recherche.'
                : 'Aucun doublon n\'a été détecté sur cette période. Le système fonctionne normalement et les agents soumettent des données uniques.'
              }
            </div>
          </div>
        ) : (
          <table className="tableau-doublons-moderne">
            <thead>
              <tr>
                <th>Date de soumission</th>
                <th>Produit</th>
                <th>Ville</th>
                <th>Prix soumis</th>
                <th>Agent</th>
              </tr>
            </thead>
            <tbody>
              {doublonsFiltres.map((doublon) => (
                <tr key={doublon.id}>
                  <td>
                    <div className="cellule-icone">
                      <Calendar size={16} />
                      {formaterDate(doublon.date_heure)}
                    </div>
                  </td>
                  <td>
                    <div className="cellule-icone">
                      <Package size={16} />
                      <span className="cellule-produit-doublon">{doublon.produit_nom}</span>
                    </div>
                  </td>
                  <td>
                    <div className="cellule-icone">
                      <MapPin size={16} />
                      {doublon.ville_nom}
                    </div>
                  </td>
                  <td>
                    <span className="cellule-prix-doublon">
                      {doublon.prix.toLocaleString('fr-FR')} Ar
                    </span>
                  </td>
                  <td>
                    <div className="cellule-icone">
                      <User size={16} />
                      {doublon.agent_nom}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Section explicative sur le fonctionnement de Rabin-Karp. */}
      <div className="section-info-rabin-karp">
        <div className="icone-info-rabin">
          <Info size={24} />
        </div>
        <div className="contenu-info-rabin">
          <div className="titre-info-rabin">À propos de la détection de doublons</div>
          <div className="texte-info-rabin">
            Le système utilise l'algorithme Rabin-Karp pour détecter automatiquement 
            les rapports identiques soumis dans les vingt-quatre heures précédentes. 
            Chaque rapport est transformé en une empreinte numérique unique via une 
            fonction de hachage, puis comparé aux empreintes des soumissions récentes. 
            En cas de correspondance, le rapport est marqué comme doublon et n'est 
            pas intégré aux statistiques du système, mais il reste enregistré pour 
            permettre cette surveillance.
          </div>
        </div>
      </div>
    </div>
  );
}

export default PageSurveillanceDoublons;