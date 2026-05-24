// Page de surveillance des doublons pour l'administrateur de Tsenan'tsika.
// Cette page affiche tous les rapports de prix qui ont été détectés
// comme dupliqués par l'algorithme Rabin-Karp lors de leur soumission.
// L'administrateur peut analyser ces doublons pour identifier d'éventuels
// comportements problématiques chez certains agents ou des dysfonctionnements
// techniques dans le système de collecte.

import { useState, useEffect } from 'react';
import {
  ShieldAlert, Calendar, MapPin, Package,
  User, Filter, AlertTriangle, Search
} from 'lucide-react';
import { serviceAdmin } from '../services/api';

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
      setErreur('Impossible de charger les doublons');
      console.error(err);
    } finally {
      setChargement(false);
    }
  };

  // Filtrage des doublons selon la recherche textuelle
  const doublonsFiltres = doublons.filter(d => {
    if (!recherche) return true;
    const termeRecherche = recherche.toLowerCase();
    return (
      d.agent_nom.toLowerCase().includes(termeRecherche) ||
      d.produit_nom.toLowerCase().includes(termeRecherche) ||
      d.ville_nom.toLowerCase().includes(termeRecherche)
    );
  });

  // Calcul des statistiques de surveillance pour les administrateurs.
  // Cette analyse aide à identifier rapidement les agents les plus
  // concernés par les détections de doublons.
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

  // Formatage de la date pour un affichage lisible en français
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
      <div className="carte">
        <h2>Surveillance des doublons</h2>
        <div className="message-info">Chargement en cours...</div>
      </div>
    );
  }

  return (
    <div>
      {/* Carte d'en-tête avec titre et description du rôle de cette page */}
      <div className="carte">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ShieldAlert size={28} />
              Surveillance des doublons
            </h2>
            <p style={{ color: '#6b7280', marginTop: '0.5rem' }}>
              Consultez les rapports identifiés comme doublons par l'algorithme Rabin-Karp 
              pour analyser les comportements de soumission et détecter d'éventuelles anomalies.
            </p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#dc2626' }}>
              {doublons.length}
            </div>
            <div style={{ fontSize: '0.9rem', color: '#6b7280' }}>
              doublons sur {periodeJours} jours
            </div>
          </div>
        </div>
      </div>

      {/* Carte de statistiques rapides pour identifier les patterns */}
      {agentsAvecPlusDeDoublons.length > 0 && (
        <div className="carte">
          <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={20} color="#f59e0b" />
            Agents avec le plus de doublons détectés
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            {agentsAvecPlusDeDoublons.map((agent, index) => (
              <div
                key={agent.id}
                style={{
                  padding: '1rem',
                  backgroundColor: index === 0 ? '#fef3c7' : '#f3f4f6',
                  borderRadius: '0.5rem',
                  borderLeft: `4px solid ${index === 0 ? '#f59e0b' : '#9ca3af'}`
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <User size={16} />
                  <strong>{agent.nom}</strong>
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937' }}>
                  {agent.nombre} doublon{agent.nombre > 1 ? 's' : ''}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Carte de filtres pour la période et la recherche */}
      <div className="carte">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 200px', gap: '1rem' }}>
          <div style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#9ca3af' }} />
            <input
              type="text"
              placeholder="Rechercher par agent, produit ou ville..."
              value={recherche}
              onChange={(e) => setRecherche(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem 0.75rem 0.75rem 2.5rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                fontSize: '0.95rem'
              }}
            />
          </div>
          <select
            value={periodeJours}
            onChange={(e) => setPeriodeJours(parseInt(e.target.value))}
            style={{
              padding: '0.75rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.375rem',
              fontSize: '0.95rem'
            }}
          >
            <option value={7}>7 derniers jours</option>
            <option value={30}>30 derniers jours</option>
            <option value={90}>90 derniers jours</option>
            <option value={365}>1 année</option>
          </select>
        </div>
      </div>

      {/* Carte avec la liste détaillée des doublons */}
      <div className="carte">
        {erreur && <div className="message-erreur">{erreur}</div>}
        
        {doublonsFiltres.length === 0 ? (
          <div className="message-info">
            {recherche 
              ? 'Aucun doublon ne correspond aux critères de recherche.'
              : 'Aucun doublon détecté sur cette période. Le système fonctionne normalement.'
            }
          </div>
        ) : (
          <table className="tableau-donnees">
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
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Calendar size={16} color="#6b7280" />
                      {formaterDate(doublon.date_heure)}
                    </div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Package size={16} color="#6b7280" />
                      <strong>{doublon.produit_nom}</strong>
                    </div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <MapPin size={16} color="#6b7280" />
                      {doublon.ville_nom}
                    </div>
                  </td>
                  <td>
                    <strong style={{ color: '#dc2626' }}>
                      {doublon.prix.toLocaleString('fr-FR')} Ar
                    </strong>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <User size={16} color="#6b7280" />
                      {doublon.agent_nom}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Section d'explication pédagogique sur le fonctionnement de la détection */}
      <div className="carte">
        <h3 style={{ marginBottom: '0.5rem' }}>À propos de la détection de doublons</h3>
        <p style={{ color: '#4b5563', lineHeight: '1.6' }}>
          Le système utilise l'algorithme Rabin-Karp pour détecter automatiquement 
          les rapports identiques soumis dans les vingt-quatre heures précédentes. 
          Chaque rapport est transformé en une empreinte numérique unique, puis 
          comparé aux empreintes des soumissions récentes. En cas de correspondance, 
          le rapport est marqué comme doublon et n'est pas intégré aux statistiques 
          du système, mais il reste enregistré pour permettre cette surveillance.
        </p>
      </div>
    </div>
  );
}

export default PageSurveillanceDoublons;