import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Sprout, LayoutDashboard, PlusCircle, Route,
  LogOut, User, Users, ShieldAlert, Sun, Moon
} from 'lucide-react';
import { serviceAuth } from '../services/api';
import { utiliserTheme } from '../contexts/ContexteTheme';
import '../styles/MisePage.css';

function MisePage({ children }) {
  const emplacement = useLocation();
  
  const naviguer = useNavigate();
  
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  const { theme, basculerTheme } = utiliserTheme();
  
  const gererDeconnexion = () => {
    serviceAuth.seDeconnecter();
    naviguer('/connexion');
  };
  
  const construireLiens = () => {
    const liens = [];
    
    if (utilisateur) {
      liens.push({
        chemin: '/tableau-bord',
        libelle: 'Tableau de bord',
        icone: LayoutDashboard
      });
    }
    
    if (utilisateur && utilisateur.role === 'agent') {
      liens.push({
        chemin: '/saisie',
        libelle: 'Saisie de prix',
        icone: PlusCircle
      });
    }
    
    if (utilisateur && (utilisateur.role === 'analyste')) {
      liens.push({
        chemin: '/itineraire',
        libelle: 'Itinéraire optimal',
        icone: Route
      });
    }
    
    if (utilisateur && utilisateur.role === 'administrateur') {
      liens.push({
        chemin: '/admin/utilisateurs',
        libelle: 'Gestion des utilisateurs',
        icone: Users
      });
    }

    if (utilisateur && utilisateur.role === 'administrateur') {
      liens.push({
        chemin: '/admin/doublons',
        libelle: 'Surveillance doublons',
        icone: ShieldAlert
      });
    }
    return liens;
  };
  
  const obtenirInitiales = () => {
    if (!utilisateur) return '?';
    const premierePrenoms = utilisateur.prenoms?.charAt(0) || '';
    const premierNom = utilisateur.nom?.charAt(0) || '';
    return (premierePrenoms + premierNom).toUpperCase();
  };
  
  const liens = construireLiens();

  return (
    <div className="mise-page">
      
      {/* Barre de navigation principale en haut de la page. */}
      <nav className="barre-navigation">
        <div className="contenu-navigation">
          
          {/* Logo et nom de l'application à gauche. */}
          <Link to="/" className="logo-navigation">
            <div className="icone-logo-nav">
              <Sprout size={22} strokeWidth={2.5} />
            </div>
            <div className="texte-logo-nav">
              <span className="nom-app-nav">Tsenan'tsika</span>
              <span className="sous-titre-nav">Surveillance des prix</span>
            </div>
          </Link>
          
          {/* Menu de navigation au centre adapté au rôle. */}
          <ul className="menu-navigation">
            {liens.map((lien) => {
              const IconeComposant = lien.icone;
              const estActif = emplacement.pathname === lien.chemin;
              
              return (
                <li key={lien.chemin}>
                  <Link
                    to={lien.chemin}
                    className={`lien-navigation ${estActif ? 'actif' : ''}`}
                  >
                    <IconeComposant size={18} />
                    <span>{lien.libelle}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
          
          {/* Profil de l'utilisateur connecté à droite avec bouton de déconnexion. */}
          <div className="profil-utilisateur">
            <div className="info-utilisateur">
              <span className="nom-utilisateur">
                {utilisateur ? `${utilisateur.prenoms} ${utilisateur.nom}` : 'Utilisateur'}
              </span>
              <span className="role-utilisateur">
                {utilisateur ? utilisateur.role : ''}
              </span>
            </div>
            <div className="avatar-utilisateur">
              {obtenirInitiales()}
            </div>
            <button
              type="button"
              className="bouton-theme"
              onClick={basculerTheme}
              title={theme === 'clair' ? 'Passer en mode sombre' : 'Passer en mode clair'}
            >
              {theme === 'clair' ? <Moon size={18} /> : <Sun size={18} />}
            </button>
            <button
              type="button"
              className="bouton-deconnexion"
              onClick={gererDeconnexion}
              title="Se déconnecter"
            >
              <LogOut size={16} />
              <span>Déconnexion</span>
            </button>
          </div>
        </div>
      </nav>
      
      {/* Zone principale où s'affiche le contenu de la page courante. */}
      <main className="zone-principale">
        {children}
      </main>
      
      {/* Pied de page institutionnel discret en bas. */}
      <footer className="pied-page">
        <div className="contenu-pied">
          <div className="copyright-pied">
            Tsenan'tsika 2026 - Système national de surveillance des prix alimentaires
          </div>
          <div className="liens-pied">
            <span>Projet transversal L2</span>
            <span>ESMIA Innovation</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default MisePage;