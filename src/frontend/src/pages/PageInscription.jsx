// Page d'inscription des citoyens de Tsenan'tsika.
// Cette page permet aux citoyens malgaches de créer leur propre compte
// pour accéder en consultation au système de surveillance des prix.
// Les autres rôles comme agent, analyste et administrateur sont créés
// uniquement par l'administrateur du système, conformément au cahier
// des charges et aux bonnes pratiques de gestion des accès.

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Sprout, User, Mail, Lock, ArrowRight, AlertCircle,
  CheckCircle2, Eye, ShieldCheck, TrendingUp, Bell
} from 'lucide-react';
import { serviceAuth } from '../services/api';
import '../styles/Auth.css';

function PageInscription() {
  const navigate = useNavigate();
  
  // États du formulaire qui stockent toutes les informations saisies
  // par le futur utilisateur citoyen. Nous séparons chaque champ dans
  // son propre état pour permettre des validations indépendantes.
  const [nom, setNom] = useState('');
  const [prenoms, setPrenoms] = useState('');
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [confirmationMotDePasse, setConfirmationMotDePasse] = useState('');
  const [erreur, setErreur] = useState(null);
  const [chargement, setChargement] = useState(false);

  // Validation côté client qui vérifie la cohérence des données avant
  // d'envoyer la requête au backend. Cette validation immédiate offre
  // un meilleur retour à l'utilisateur que d'attendre la réponse du serveur.
  const validerFormulaire = () => {
    if (nom.length < 2) {
      setErreur('Le nom doit comporter au moins 2 caractères.');
      return false;
    }
    if (prenoms.length < 2) {
      setErreur('Les prénoms doivent comporter au moins 2 caractères.');
      return false;
    }
    if (motDePasse.length < 8) {
      setErreur('Le mot de passe doit comporter au moins 8 caractères.');
      return false;
    }
    if (motDePasse !== confirmationMotDePasse) {
      setErreur('Les mots de passe ne correspondent pas.');
      return false;
    }
    return true;
  };

  // Gestionnaire de soumission qui valide les données puis appelle
  // le service d'authentification pour créer le nouveau compte citoyen.
  const gererInscription = async (evenement) => {
    evenement.preventDefault();
    setErreur(null);
    
    if (!validerFormulaire()) {
      return;
    }
    
    setChargement(true);
    
    try {
      const resultat = await serviceAuth.sInscrire(nom, prenoms, email, motDePasse);
      
      // Après une inscription réussie, l'utilisateur est automatiquement
      // connecté grâce au token retourné par le backend. On le redirige
      // vers le tableau de bord qui est la page principale des citoyens.
      navigate('/tableau-bord');
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setErreur('Un utilisateur avec cet email existe déjà. Veuillez vous connecter.');
      } else {
        setErreur('Impossible de créer le compte. Vérifiez que le serveur est démarré.');
      }
      console.error('Erreur d\'inscription:', err);
    } finally {
      setChargement(false);
    }
  };

  // Variants d'animation pour orchestrer l'apparition séquentielle
  // des différents éléments de la page de manière harmonieuse.
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
      
      {/* Section gauche de présentation qui met en avant les avantages
          de créer un compte sur le système Tsenan'tsika. */}
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
            Rejoignez la <span className="accent">communauté</span> au service de la transparence
          </h1>
          <p className="description-presentation">
            En tant que citoyen, créez votre compte gratuit pour consulter
            en temps réel les prix des produits alimentaires sur les marchés
            malgaches et être informé des anomalies détectées par notre
            système d'analyse automatique.
          </p>
        </motion.div>

        <motion.div variants={elementVariants}>
          <div className="avantages-inscription">
            <div className="avantage-item">
              <div className="icone-avantage">
                <Eye size={20} />
              </div>
              <div>
                <div className="titre-avantage">Consultation en temps réel</div>
                <div className="description-avantage">
                  Accédez aux prix actuels sur les sept villes pilotes
                </div>
              </div>
            </div>
            
            <div className="avantage-item">
              <div className="icone-avantage">
                <Bell size={20} />
              </div>
              <div>
                <div className="titre-avantage">Alertes automatiques</div>
                <div className="description-avantage">
                  Soyez informé des anomalies de prix détectées par le système
                </div>
              </div>
            </div>
            
            <div className="avantage-item">
              <div className="icone-avantage">
                <TrendingUp size={20} />
              </div>
              <div>
                <div className="titre-avantage">Tendances et statistiques</div>
                <div className="description-avantage">
                  Suivez l'évolution des prix sur différentes périodes
                </div>
              </div>
            </div>
          </div>
          
          <div className="mention-presentation">
            <ShieldCheck size={14} />
            Inscription gratuite et sécurisée pour les citoyens
          </div>
        </motion.div>
      </motion.section>

      {/* Section droite contenant le formulaire d'inscription. */}
      <section className="section-formulaire">
        <motion.div
          className="conteneur-formulaire"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, ease: [0.4, 0, 0.2, 1] }}
        >
          <div className="entete-formulaire">
            <h2 className="titre-formulaire">Créez votre compte</h2>
            <p className="description-formulaire">
              Quelques informations suffisent pour rejoindre Tsenan'tsika.
            </p>
          </div>

          <form onSubmit={gererInscription}>
            
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

            {/* Champs nom et prénoms côte à côte pour optimiser l'espace.
                Cette disposition en deux colonnes est typique des formulaires
                d'inscription modernes. */}
            <div className="ligne-champs">
              <div className="groupe-champ">
                <label className="label-champ" htmlFor="nom">
                  Nom
                </label>
                <div className="conteneur-input">
                  <User size={18} className="icone-input" />
                  <input
                    id="nom"
                    type="text"
                    className="input-moderne"
                    placeholder="Rakoto"
                    value={nom}
                    onChange={(e) => setNom(e.target.value)}
                    required
                    disabled={chargement}
                  />
                </div>
              </div>

              <div className="groupe-champ">
                <label className="label-champ" htmlFor="prenoms">
                  Prénoms
                </label>
                <div className="conteneur-input">
                  <User size={18} className="icone-input" />
                  <input
                    id="prenoms"
                    type="text"
                    className="input-moderne"
                    placeholder="Jean Paul"
                    value={prenoms}
                    onChange={(e) => setPrenoms(e.target.value)}
                    required
                    disabled={chargement}
                  />
                </div>
              </div>
            </div>

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
                  placeholder="Minimum 8 caractères"
                  value={motDePasse}
                  onChange={(e) => setMotDePasse(e.target.value)}
                  required
                  disabled={chargement}
                />
              </div>
            </div>

            <div className="groupe-champ">
              <label className="label-champ" htmlFor="confirmation">
                Confirmer le mot de passe
              </label>
              <div className="conteneur-input">
                <Lock size={18} className="icone-input" />
                <input
                  id="confirmation"
                  type="password"
                  className="input-moderne"
                  placeholder="Retapez votre mot de passe"
                  value={confirmationMotDePasse}
                  onChange={(e) => setConfirmationMotDePasse(e.target.value)}
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
                  Création du compte...
                </>
              ) : (
                <>
                  Créer mon compte citoyen
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <p className="lien-alternatif">
            Vous avez déjà un compte ?{' '}
            <Link to="/connexion">Connectez-vous</Link>
          </p>

          <div className="information-roles">
            <CheckCircle2 size={14} />
            <span>
              L'inscription libre est réservée aux citoyens. Les comptes
              d'agents et d'analystes sont créés par l'administrateur.
            </span>
          </div>
        </motion.div>
      </section>
    </div>
  );
}

export default PageInscription;