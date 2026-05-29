import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  LayoutDashboard, PlusCircle, Route, Users, ShieldAlert,
  ArrowRight, Sparkles, MapPin, Package, AlertCircle,
  TrendingUp
} from 'lucide-react';
import { serviceAuth, serviceTableauBord, servicePrix } from '../services/api';
import '../styles/PageAccueil.css';

function PageAccueil() {
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  const [statistiques, setStatistiques] = useState({
    alertes: 0,
    villes: 0,
    produits: 0
  });

  useEffect(() => {
    const chargerStatistiques = async () => {
      try {
        const [tableauBord, villes, produits] = await Promise.all([
          serviceTableauBord.obtenirTableauBord(),
          servicePrix.listerVilles(),
          servicePrix.listerProduits()
        ]);
        
        setStatistiques({
          alertes: tableauBord.nombre_alertes_actives,
          villes: villes.length,
          produits: produits.length
        });
      } catch (err) {
        console.error('Erreur lors du chargement des statistiques:', err);
      }
    };

    chargerStatistiques();
  }, []);

  const peutVoirSaisie = utilisateur && utilisateur.role === 'agent';
  const peutVoirItineraire = utilisateur && 
    (utilisateur.role === 'analyste');
  const estAdministrateur = utilisateur && utilisateur.role === 'administrateur';

  const obtenirSalutation = () => {
    const heure = new Date().getHours();
    if (heure < 12) return 'Bonjour';
    if (heure < 18) return 'Bon après-midi';
    return 'Bonsoir';
  };

  return (
    <div className="page-accueil">
      
      {/* Bannière d'accueil personnalisée qui salue l'utilisateur. */}
      <section className="banniere-accueil">
        <div className="contenu-banniere">
          <div className="salutation-utilisateur">
            <Sparkles size={16} />
            <span>{obtenirSalutation()}, {utilisateur?.prenoms}</span>
          </div>
          
          <h1 className="titre-banniere">
            Bienvenue sur <span className="accent-banniere">Tsenan'tsika</span>
          </h1>
          
          <p className="description-banniere">
            Le système national de surveillance des prix alimentaires de Madagascar 
            vous accompagne pour suivre, analyser et protéger le pouvoir d'achat 
            des citoyens à travers les sept villes pilotes du pays.
          </p>
          
          <div className="badge-role">
            <span>Connecté en tant que {utilisateur?.role}</span>
          </div>
        </div>
      </section>

      {/* Grille des statistiques rapides du système. */}
      <section className="statistiques-rapides">
        <div className="carte-statistique">
          <div className="icone-statistique alerte">
            <AlertCircle size={28} />
          </div>
          <div className="contenu-statistique">
            <div className="valeur-statistique-accueil">{statistiques.alertes}</div>
            <div className="label-statistique-accueil">Alertes actives</div>
          </div>
        </div>
        
        <div className="carte-statistique">
          <div className="icone-statistique primaire">
            <MapPin size={28} />
          </div>
          <div className="contenu-statistique">
            <div className="valeur-statistique-accueil">{statistiques.villes}</div>
            <div className="label-statistique-accueil">Villes pilotes</div>
          </div>
        </div>
        
        <div className="carte-statistique">
          <div className="icone-statistique secondaire">
            <Package size={28} />
          </div>
          <div className="contenu-statistique">
            <div className="valeur-statistique-accueil">{statistiques.produits}</div>
            <div className="label-statistique-accueil">Produits suivis</div>
          </div>
        </div>
        
        <div className="carte-statistique">
          <div className="icone-statistique tertiaire">
            <TrendingUp size={28} />
          </div>
          <div className="contenu-statistique">
            <div className="valeur-statistique-accueil">24h</div>
            <div className="label-statistique-accueil">Détection temps réel</div>
          </div>
        </div>
      </section>

      {/* Section des fonctionnalités disponibles selon le rôle. */}
      <section className="section-fonctionnalites">
        <h2 className="titre-section">Vos fonctionnalités</h2>
        <p className="description-section">
          Accédez rapidement aux outils mis à votre disposition selon votre rôle dans le système.
        </p>
        
        <div className="grille-fonctionnalites">
          
          {/* Tableau de bord accessible à tous les utilisateurs connectés. */}
          <Link to="/tableau-bord" className="carte-fonctionnalite">
            <div className="entete-carte-fonctionnalite">
              <div className="icone-fonctionnalite couleur-primaire">
                <LayoutDashboard size={24} />
              </div>
              <h3 className="titre-fonctionnalite">Tableau de bord</h3>
            </div>
            <p className="description-fonctionnalite">
              Consultez en temps réel les alertes de prix anormaux et le classement 
              des produits avec les plus fortes hausses observées sur les marchés.
            </p>
            <span className="lien-fonctionnalite">
              Accéder <ArrowRight size={16} />
            </span>
          </Link>

          {/* Saisie de prix réservée aux agents de collecte. */}
          {peutVoirSaisie && (
            <Link to="/saisie" className="carte-fonctionnalite">
              <div className="entete-carte-fonctionnalite">
                <div className="icone-fonctionnalite couleur-secondaire">
                  <PlusCircle size={24} />
                </div>
                <h3 className="titre-fonctionnalite">Saisie de prix</h3>
              </div>
              <p className="description-fonctionnalite">
                Soumettez les prix observés sur les marchés locaux. Le système 
                détecte automatiquement les doublons et calcule les variations.
              </p>
              <span className="lien-fonctionnalite">
                Saisir un prix <ArrowRight size={16} />
              </span>
            </Link>
          )}

          {/* Calcul d'itinéraire réservé aux analystes et administrateurs. */}
          {peutVoirItineraire && (
            <Link to="/itineraire" className="carte-fonctionnalite">
              <div className="entete-carte-fonctionnalite">
                <div className="icone-fonctionnalite couleur-tertiaire">
                  <Route size={24} />
                </div>
                <h3 className="titre-fonctionnalite">Itinéraire optimal</h3>
              </div>
              <p className="description-fonctionnalite">
                Calculez la route d'approvisionnement la moins coûteuse entre 
                deux villes du réseau routier malgache via Dijkstra.
              </p>
              <span className="lien-fonctionnalite">
                Calculer un itinéraire <ArrowRight size={16} />
              </span>
            </Link>
          )}

          {/* Gestion des utilisateurs réservée à l'administrateur. */}
          {estAdministrateur && (
            <Link to="/admin/utilisateurs" className="carte-fonctionnalite">
              <div className="entete-carte-fonctionnalite">
                <div className="icone-fonctionnalite couleur-primaire">
                  <Users size={24} />
                </div>
                <h3 className="titre-fonctionnalite">Gestion des utilisateurs</h3>
              </div>
              <p className="description-fonctionnalite">
                Créez, modifiez et désactivez les comptes des agents, analystes 
                et citoyens du système.
              </p>
              <span className="lien-fonctionnalite">
                Gérer les comptes <ArrowRight size={16} />
              </span>
            </Link>
          )}

          {/* Surveillance des doublons réservée à l'administrateur. */}
          {estAdministrateur && (
            <Link to="/admin/doublons" className="carte-fonctionnalite">
              <div className="entete-carte-fonctionnalite">
                <div className="icone-fonctionnalite couleur-secondaire">
                  <ShieldAlert size={24} />
                </div>
                <h3 className="titre-fonctionnalite">Surveillance des doublons</h3>
              </div>
              <p className="description-fonctionnalite">
                Consultez les rapports détectés comme doublons par Rabin-Karp 
                pour identifier les comportements anormaux.
              </p>
              <span className="lien-fonctionnalite">
                Surveiller les doublons <ArrowRight size={16} />
              </span>
            </Link>
          )}
        </div>
      </section>
    </div>
  );
}

export default PageAccueil;