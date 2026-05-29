import { useState, useEffect } from 'react';
import {
  LayoutDashboard, AlertTriangle, TrendingUp, Sparkles,
  Calendar, MapPin, Info, Activity, Download
} from 'lucide-react';
import { serviceAuth, serviceTableauBord, serviceExport } from '../services/api';
import '../styles/PageTableauBord.css';

function PageTableauBord() {
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  const [donnees, setDonnees] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);
  const [exportEnCours, setExportEnCours] = useState(false);
  const [erreurExport, setErreurExport] = useState(null);

  useEffect(() => {
    const recupererDonnees = async () => {
      try {
        const reponse = await serviceTableauBord.obtenirTableauBord();
        setDonnees(reponse);
        setErreur(null);
      } catch (err) {
        setErreur('Impossible de charger le tableau de bord. Vérifiez que le serveur backend est démarré.');
        console.error('Erreur lors du chargement du tableau de bord:', err);
      } finally {
        setChargement(false);
      }
    };

    recupererDonnees();
  }, []);

    const gererExportPdf = async () => {
      setExportEnCours(true);
      setErreurExport(null);
      try {
        await serviceExport.telechargerRapportPdf();
      } catch (err) {
        setErreurExport("Impossible de générer le rapport PDF. Veuillez réessayer.");
        console.error('Erreur lors de l\'export PDF:', err);
      } finally {
        setExportEnCours(false);
      }
    };

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

    const obtenirClasseRang = (rang) => {
      if (rang === 1) return 'rang-1';
      if (rang === 2) return 'rang-2';
      if (rang === 3) return 'rang-3';
      return 'rang-autre';
    };

    const obtenirMessageTopKVide = () => {
      if (utilisateur && utilisateur.role === 'agent') {
        return {
          titre: "Aucune variation enregistrée",
          description: "Effectuez quelques saisies de prix pour alimenter le classement des hausses."
        };
      }
      if (utilisateur && utilisateur.role === 'administrateur') {
        return {
          titre: "Aucune variation significative",
          description: "Le classement se remplira automatiquement lorsque les agents soumettront des prix présentant des écarts notables."
        };
      }
      return {
        titre: "Marché stable",
        description: "Aucune variation significative n'a été enregistrée récemment. Cette section se mettra à jour automatiquement dès que des écarts notables seront détectés sur les marchés."
      };
    };

  if (chargement) {
    return (
      <div className="entete-tableau-bord">
        <div className="contenu-entete-tableau">
          <h1 className="titre-tableau-bord">
            <span className="icone-titre-tableau">
              <LayoutDashboard size={24} />
            </span>
            Tableau de bord
          </h1>
          <p className="description-tableau-bord">Chargement des données en cours...</p>
        </div>
      </div>
    );
  }

  if (erreur) {
    return (
      <div className="entete-tableau-bord">
        <div className="contenu-entete-tableau">
          <h1 className="titre-tableau-bord">
            <span className="icone-titre-tableau">
              <LayoutDashboard size={24} />
            </span>
            Tableau de bord
          </h1>
          <p className="description-tableau-bord" style={{ color: 'var(--erreur)' }}>
            {erreur}
          </p>
        </div>
      </div>
    );
  }

  const messageTopKVide = obtenirMessageTopKVide();

  return (
    <div className="page-tableau-bord">
      
      {/* En-tête principal avec titre et compteur d'alertes proéminent. */}
      <div className="entete-tableau-bord">
        <div className="contenu-entete-tableau">
          <h1 className="titre-tableau-bord">
            <span className="icone-titre-tableau">
              <LayoutDashboard size={24} />
            </span>
            Tableau de bord
          </h1>
          <p className="description-tableau-bord">
            Vue synthétique de l'activité du système de surveillance des prix 
            alimentaires sur les sept derniers jours.
          </p>
        </div>
        {utilisateur?.role === 'analyste' && (
            <button
              className="bouton-export-pdf"
              onClick={gererExportPdf}
              disabled={exportEnCours}
            >
              <Download size={18} />
              {exportEnCours ? 'Génération...' : 'Exporter en PDF'}
            </button>
          )}

        {erreurExport && (
          <div className="message-erreur-export">
            {erreurExport}
          </div>
        )}
        
        <div className="compteur-alertes-principal">
          <div className="nombre-alertes-grand">
            {donnees.nombre_alertes_actives}
          </div>
          <div className="label-alertes-grand">
            Alertes actives
          </div>
        </div>
      </div>

      {/* Grille principale avec les alertes et le Top-k côte à côte. */}
      <div className="grille-tableau-bord">
        
        {/* Section des alertes récentes avec design moderne. */}
        <div className="section-donnees">
          <div className="entete-section-donnees">
            <h2 className="titre-section-donnees">
              <AlertTriangle size={20} color="var(--erreur)" />
              Alertes récentes
            </h2>
            <span className="compteur-section">
              {donnees.alertes_recentes.length}
            </span>
          </div>
          
          {donnees.alertes_recentes.length === 0 ? (
            <div className="message-etat-vide">
              <div className="icone-etat-vide">
                <Activity size={32} />
              </div>
              <div className="titre-etat-vide">Système stable</div>
              <div className="description-etat-vide">
                Aucune alerte de prix anormal n'a été déclenchée récemment.
              </div>
            </div>
          ) : (
            <div className="liste-alertes">
              {donnees.alertes_recentes.map((alerte) => (
                <div key={alerte.id} className="carte-alerte-moderne">
                  <div className="entete-alerte">
                    <div className="contenu-alerte">
                      <span className="produit-alerte">{alerte.produit_nom}</span>
                      <span className="ville-alerte">à {alerte.ville_nom}</span>
                    </div>
                  </div>
                  <div className="date-alerte">
                    <Calendar size={12} />
                    Déclenchée le {formaterDate(alerte.date)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section du classement Top-k avec design en podium. */}
        <div className="section-donnees">
          <div className="entete-section-donnees">
            <h2 className="titre-section-donnees">
              <TrendingUp size={20} color="var(--avertissement)" />
              Top 5 des hausses
            </h2>
            <span className="compteur-section">
              {donnees.top_5_hausses.length} / 5
            </span>
          </div>
          
          {donnees.top_5_hausses.length === 0 ? (
            <div className="message-etat-vide">
              <div className="icone-etat-vide">
                <Sparkles size={32} />
              </div>
              <div className="titre-etat-vide">{messageTopKVide.titre}</div>
              <div className="description-etat-vide">{messageTopKVide.description}</div>
            </div>
          ) : (
            <div className="liste-top-k">
              {donnees.top_5_hausses.map((entree) => (
                <div key={entree.produit_id} className="entree-top-k-moderne">
                  <div className={`rang-top-k ${obtenirClasseRang(entree.rang)}`}>
                    {entree.rang}
                  </div>
                  <div className="contenu-top-k">
                    <div className="nom-produit-top-k">{entree.produit_nom}</div>
                    <div className="variation-top-k">
                      <TrendingUp size={16} />
                      +{entree.variation_pourcent}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Section explicative en bas pour contextualiser le tableau de bord. */}
      <div className="section-explicative">
        <div className="icone-info">
          <Info size={24} />
        </div>
        <div className="contenu-explicatif">
          <div className="titre-explicatif">Comment fonctionne ce tableau de bord</div>
          <div className="texte-explicatif">
            Tsenan'tsika analyse en continu les prix soumis par les agents de collecte 
            répartis dans les sept villes pilotes. Quand un nouveau prix présente une 
            variation supérieure à 20% par rapport à la moyenne récente, une alerte 
            est automatiquement déclenchée. Le classement Top 5 maintient en temps réel 
            les produits ayant connu les plus fortes hausses, permettant d'identifier 
            rapidement les situations nécessitant une intervention prioritaire.
          </div>
        </div>
      </div>
    </div>
  );
}

export default PageTableauBord;