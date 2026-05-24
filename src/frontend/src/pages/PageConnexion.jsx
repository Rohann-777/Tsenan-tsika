// Page de connexion de Tsenan'tsika.
// Cette page permet aux utilisateurs existants de s'authentifier au
// système en utilisant leur email et leur mot de passe. Elle suit
// les principes de design moderne avec une mise en page en deux
// colonnes et des animations soignées pour créer une expérience
// utilisateur premium.

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Sprout, Mail, Lock, ArrowRight, AlertCircle,
  Users, MapPin, Package, KeyRound
} from 'lucide-react';
import { serviceAuth } from '../services/api';
import '../styles/Auth.css';

function PageConnexion() {
  const navigate = useNavigate();
  
  // États du formulaire qui stockent les valeurs saisies par l'utilisateur
  // et gèrent les différentes phases du processus de connexion.
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [erreur, setErreur] = useState(null);
  const [chargement, setChargement] = useState(false);

  // Gestionnaire de soumission qui appelle le service d'authentification
  // et redirige l'utilisateur vers la page appropriée selon son rôle.
  const gererConnexion = async (evenement) => {
    evenement.preventDefault();
    setErreur(null);
    setChargement(true);
    
    try {
      const resultat = await serviceAuth.seConnecter(email, motDePasse);
      
      // Redirection conditionnelle selon le rôle de l'utilisateur.
      // Chaque rôle a une page d'accueil par défaut qui correspond
      // à ses principales fonctionnalités dans le système.
      const role = resultat.utilisateur.role;
      if (role === 'agent') {
        navigate('/saisie');
      } else if (role === 'analyste' || role === 'administrateur') {
        navigate('/tableau-bord');
      } else {
        navigate('/');
      }
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setErreur('Email ou mot de passe incorrect. Veuillez réessayer.');
      } else {
        setErreur('Impossible de se connecter. Vérifiez que le serveur est démarré.');
      }
      console.error('Erreur de connexion:', err);
    } finally {
      setChargement(false);
    }
  };

  // Variants d'animation pour orchestrer l'apparition séquentielle
  // des différents éléments de la page selon une chorégraphie soignée.
  const conteneurVariants = {
    cache: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const elementVariants = {
    cache: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.4, 0, 0.2, 1],
      },
    },
  };

  return (
    <div className="page-auth">
      
      {/* Section gauche de présentation qui établit l'identité visuelle
          et communique les valeurs du système Tsenan'tsika. */}
      <motion.section
        className="section-presentation"
        initial="cache"
        animate="visible"
        variants={conteneurVariants}
      >
        <motion.div className="logo-section" variants={elementVariants}>
          <div className="icone-logo">
            <Sprout size={32} strokeWidth={2} />
          </div>
          <div>
            <div className="nom-application">Tsenan'tsika</div>
            <div className="sous-titre-application">
              Système national de surveillance
            </div>
          </div>
        </motion.div>

        <motion.div className="contenu-presentation" variants={elementVariants}>
          <h1 className="titre-presentation">
            Le numérique au service de la <span className="accent">sécurité alimentaire</span> à Madagascar
          </h1>
          <p className="description-presentation">
            Tsenan'tsika centralise et analyse en temps réel les prix des
            produits de première nécessité observés sur les marchés malgaches,
            permettant aux autorités d'agir rapidement face aux anomalies
            et de protéger le pouvoir d'achat des citoyens.
          </p>
        </motion.div>

        <motion.div variants={elementVariants}>
          <div className="statistiques-presentation">
            <div className="statistique">
              <span className="valeur-statistique">7</span>
              <span className="label-statistique">Villes pilotes</span>
            </div>
            <div className="statistique">
              <span className="valeur-statistique">7</span>
              <span className="label-statistique">Produits suivis</span>
            </div>
            <div className="statistique">
              <span className="valeur-statistique">24h</span>
              <span className="label-statistique">Détection alertes</span>
            </div>
          </div>
          
          <div className="mention-presentation">
            <KeyRound size={14} />
            Projet transversal ESMIA Innovation 2026
          </div>
        </motion.div>
      </motion.section>

      {/* Section droite contenant le formulaire de connexion proprement dit. */}
      <section className="section-formulaire">
        <motion.div
          className="conteneur-formulaire"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, ease: [0.4, 0, 0.2, 1] }}
        >
          <div className="entete-formulaire">
            <h2 className="titre-formulaire">Bon retour parmi nous</h2>
            <p className="description-formulaire">
              Connectez-vous à votre compte pour accéder au système.
            </p>
          </div>

          <form onSubmit={gererConnexion}>
            
            {erreur && (
              <motion.div
                className="message-erreur-auth"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <AlertCircle size={18} />
                <span>{erreur}</span>
              </motion.div>
            )}

            <div className="groupe-champ">
              <label className="label-champ" htmlFor="email">
                Adresse email
              </label>
              <div className="conteneur-input">
                <Mail size={18} className="icone-input" />
                <input
                  id="email"
                  type="email"
                  className="input-moderne"
                  placeholder="votre.email@exemple.mg"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={chargement}
                />
              </div>
            </div>

            <div className="groupe-champ">
              <label className="label-champ" htmlFor="motDePasse">
                Mot de passe
              </label>
              <div className="conteneur-input">
                <Lock size={18} className="icone-input" />
                <input
                  id="motDePasse"
                  type="password"
                  className="input-moderne"
                  placeholder="••••••••"
                  value={motDePasse}
                  onChange={(e) => setMotDePasse(e.target.value)}
                  required
                  disabled={chargement}
                />
              </div>
            </div>

            <button
              type="submit"
              className="bouton-principal"
              disabled={chargement}
            >
              {chargement ? (
                <>
                  <span className="spinner"></span>
                  Connexion en cours...
                </>
              ) : (
                <>
                  Se connecter
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <p className="lien-alternatif">
            Vous êtes un citoyen et n'avez pas encore de compte ?{' '}
            <Link to="/inscription">Créez votre compte</Link>
          </p>

          {/* Section des comptes de test pour faciliter la démonstration
              lors de la soutenance. Cette section sera retirée en production
              mais elle est très utile pendant le développement et les tests. */}
          <div className="comptes-test">
            <div className="titre-comptes-test">
              <Users size={14} />
              Comptes de démonstration
            </div>
            <div className="compte-test">
              <span>admin@tsenantsika.mg</span>
              <span className="role-compte">Admin</span>
            </div>
            <div className="compte-test">
              <span>marie.analyste@tsenantsika.mg</span>
              <span className="role-compte">Analyste</span>
            </div>
            <div className="compte-test">
              <span>sophie.agent@tsenantsika.mg</span>
              <span className="role-compte">Agent</span>
            </div>
            <div className="compte-test">
              <span>tiana.citoyen@tsenantsika.mg</span>
              <span className="role-compte">Citoyen</span>
            </div>
          </div>
        </motion.div>
      </section>
    </div>
  );
}

export default PageConnexion;