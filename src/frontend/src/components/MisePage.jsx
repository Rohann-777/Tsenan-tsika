// Composant de mise en page partagée utilisé par toutes les pages
// internes de l'application Tsenan'tsika. Ce composant fournit la
// barre de navigation et le pied de page communs, et adapte
// dynamiquement les liens de navigation selon le rôle de l'utilisateur
// connecté.

import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Sprout, LayoutDashboard, PlusCircle, Route,
  LogOut, User, Users, ShieldAlert
} from 'lucide-react';
import { serviceAuth } from '../services/api';
import '../styles/MisePage.css';

function MisePage({ children }) {
  // Récupération de la position actuelle dans l'URL pour mettre en
  // évidence le lien correspondant à la page courante dans le menu.
  const emplacement = useLocation();
  
  // Récupération de la fonction de navigation pour rediriger
  // l'utilisateur après la déconnexion.
  const naviguer = useNavigate();
  
  // Récupération des informations de l'utilisateur connecté depuis
  // le stockage local pour afficher son nom et adapter le menu.
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  
  // Gestion de la déconnexion qui vide le stockage local et redirige
  // vers la page de connexion. Cette opération est immédiate et ne
  // nécessite pas de communication avec le backend puisque les tokens
  // JWT sont sans état côté serveur.
  const gererDeconnexion = () => {
    serviceAuth.seDeconnecter();
    naviguer('/connexion');
  };
  
  // Construction dynamique de la liste des liens de navigation selon
  // le rôle de l'utilisateur. Cette adaptation contextuelle est ce qui
  // donne à l'application son caractère professionnel et personnalisé.
  const construireLiens = () => {
    const liens = [];
    
    // Le tableau de bord est accessible aux analystes, administrateurs et citoyens
    // mais pas aux agents qui doivent se concentrer sur leur tâche de saisie de prix.
    if (utilisateur) {
      liens.push({
        chemin: '/tableau-bord',
        libelle: 'Tableau de bord',
        icone: LayoutDashboard
      });
    }
    
    // La saisie de prix est réservée aux agents de collecte qui
    // sont les seuls habilités à soumettre des prix observés.
    if (utilisateur && utilisateur.role === 'agent') {
      liens.push({
        chemin: '/saisie',
        libelle: 'Saisie de prix',
        icone: PlusCircle
      });
    }
    
    // Le calcul d'itinéraire est réservé aux analystes et administrateurs
    // qui utilisent cette fonctionnalité pour planifier les opérations
    // d'approvisionnement vers les zones en pénurie.
    if (utilisateur && (utilisateur.role === 'analyste' || utilisateur.role === 'administrateur')) {
      liens.push({
        chemin: '/itineraire',
        libelle: 'Itinéraire optimal',
        icone: Route
      });
    }
    
    // La gestion des utilisateurs est réservée à l'administrateur
    // conformément à la fonctionnalité F5 du cahier des charges.
    if (utilisateur && utilisateur.role === 'administrateur') {
      liens.push({
        chemin: '/admin/utilisateurs',
        libelle: 'Gestion des utilisateurs',
        icone: Users
      });
    }

    // La surveillance des doublons est également réservée à l'administrateur
    // conformément à la fonctionnalité F4 du cahier des charges.
    if (utilisateur && utilisateur.role === 'administrateur') {
      liens.push({
        chemin: '/admin/doublons',
        libelle: 'Surveillance doublons',
        icone: ShieldAlert
      });
    }
    return liens;
  };
  
  // Récupération des initiales de l'utilisateur pour l'affichage
  // dans l'avatar circulaire. Cette technique est très utilisée
  // dans les applications professionnelles modernes.
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