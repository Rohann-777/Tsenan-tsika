import { useState, useEffect } from 'react';
import {
  Users, UserPlus, Search, Edit2, Power, X, Save,
  CheckCircle2, XCircle, AlertCircle, UserCheck, UserX
} from 'lucide-react';
import { serviceAdmin, servicePrix } from '../services/api';
import '../styles/PageGestionUtilisateurs.css';

function PageGestionUtilisateurs() {
  const [utilisateurs, setUtilisateurs] = useState([]);
  const [villes, setVilles] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);
  
  const [filtreRole, setFiltreRole] = useState('');
  const [recherche, setRecherche] = useState('');
  
  const [modalOuvert, setModalOuvert] = useState(false);
  const [utilisateurEnModification, setUtilisateurEnModification] = useState(null);
  const [formulaire, setFormulaire] = useState({
    nom: '',
    prenoms: '',
    email: '',
    mot_de_passe: '',
    role: 'agent',
    ville_assignee_id: ''
  });
  const [erreurFormulaire, setErreurFormulaire] = useState(null);
  const [soumissionFormulaire, setSoumissionFormulaire] = useState(false);

  useEffect(() => {
    chargerDonnees();
  }, []);

  const chargerDonnees = async () => {
    setChargement(true);
    try {
      const [utilisateursCharges, villesChargees] = await Promise.all([
        serviceAdmin.listerUtilisateurs(),
        servicePrix.listerVilles()
      ]);
      setUtilisateurs(utilisateursCharges);
      setVilles(villesChargees);
      setErreur(null);
    } catch (err) {
      setErreur('Impossible de charger les utilisateurs. Vérifiez que le serveur backend est démarré.');
      console.error(err);
    } finally {
      setChargement(false);
    }
  };

  const statistiques = {
    total: utilisateurs.length,
    agent: utilisateurs.filter(u => u.role === 'agent').length,
    analyste: utilisateurs.filter(u => u.role === 'analyste').length,
    citoyen: utilisateurs.filter(u => u.role === 'citoyen').length
  };

  const utilisateursFiltres = utilisateurs.filter(u => {
    const correspondRole = !filtreRole || u.role === filtreRole;
    const correspondRecherche = !recherche || 
      u.nom.toLowerCase().includes(recherche.toLowerCase()) ||
      u.prenoms.toLowerCase().includes(recherche.toLowerCase()) ||
      u.email.toLowerCase().includes(recherche.toLowerCase());
    return correspondRole && correspondRecherche;
  });

  const obtenirInitiales = (prenoms, nom) => {
    const premiereLettrePrenom = prenoms.charAt(0).toUpperCase();
    const premiereLettreNom = nom.charAt(0).toUpperCase();
    return `${premiereLettrePrenom}${premiereLettreNom}`;
  };

  const ouvrirCreation = () => {
    setUtilisateurEnModification(null);
    setFormulaire({
      nom: '',
      prenoms: '',
      email: '',
      mot_de_passe: '',
      role: 'agent',
      ville_assignee_id: ''
    });
    setErreurFormulaire(null);
    setModalOuvert(true);
  };

  const ouvrirModification = (utilisateur) => {
    setUtilisateurEnModification(utilisateur);
    setFormulaire({
      nom: utilisateur.nom,
      prenoms: utilisateur.prenoms,
      email: utilisateur.email,
      mot_de_passe: '',
      role: utilisateur.role,
      ville_assignee_id: utilisateur.ville_assignee_id || ''
    });
    setErreurFormulaire(null);
    setModalOuvert(true);
  };

  const soumettreFormulaire = async (e) => {
  e.preventDefault();
  setErreurFormulaire(null);
  setSoumissionFormulaire(true);
  
  try {
    if (utilisateurEnModification) {
      // En mode modification, on construit le payload en n'incluant que
      // les champs qui ont effectivement été modifiés par l'administrateur.
      // Cela évite d'envoyer des valeurs inutiles qui pourraient déclencher
      // des validations strictes côté backend.
      const donnees = {};
      
      if (formulaire.nom !== utilisateurEnModification.nom) {
        donnees.nom = formulaire.nom;
      }
      if (formulaire.prenoms !== utilisateurEnModification.prenoms) {
        donnees.prenoms = formulaire.prenoms;
      }
      if (formulaire.email !== utilisateurEnModification.email) {
        donnees.email = formulaire.email;
      }
      if (formulaire.role !== utilisateurEnModification.role) {
        donnees.role = formulaire.role;
      }
      if (formulaire.mot_de_passe) {
        donnees.mot_de_passe = formulaire.mot_de_passe;
      }
      
      // La ville assignée n'est envoyée que si le rôle est ou devient agent.
      // Sinon, on ne touche pas à ce champ pour éviter les erreurs de validation.
      if (formulaire.role === 'agent' && formulaire.ville_assignee_id) {
        const nouvelleVilleId = parseInt(formulaire.ville_assignee_id);
        if (nouvelleVilleId !== utilisateurEnModification.ville_assignee_id) {
          donnees.ville_assignee_id = nouvelleVilleId;
        }
      }
      
      // Si aucun champ n'a été modifié, on ferme simplement le modal.
      if (Object.keys(donnees).length === 0) {
        setModalOuvert(false);
        setSoumissionFormulaire(false);
        return;
      }
      
      await serviceAdmin.modifierUtilisateur(utilisateurEnModification.id, donnees);
    } else {
      // En mode création, tous les champs requis doivent être présents.
      if (!formulaire.mot_de_passe) {
        setErreurFormulaire('Le mot de passe est obligatoire pour un nouveau compte');
        setSoumissionFormulaire(false);
        return;
      }
      
      const donnees = {
        nom: formulaire.nom,
        prenoms: formulaire.prenoms,
        email: formulaire.email,
        mot_de_passe: formulaire.mot_de_passe,
        role: formulaire.role,
        ville_assignee_id: formulaire.role === 'agent' 
          ? parseInt(formulaire.ville_assignee_id) || null 
          : null
      };
      
      await serviceAdmin.creerUtilisateur(donnees);
    }
    
    setModalOuvert(false);
    await chargerDonnees();
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      setErreurFormulaire(err.response.data.detail);
    } else {
      setErreurFormulaire('Une erreur est survenue lors de l\'enregistrement');
    }
  } finally {
    setSoumissionFormulaire(false);
  }
};

  const basculerStatut = async (utilisateur) => {
    const action = utilisateur.statut_compte ? 'désactiver' : 'activer';
    const confirmation = window.confirm(
      `Êtes-vous sûr de vouloir ${action} le compte de ${utilisateur.prenoms} ${utilisateur.nom} ?`
    );
    
    if (!confirmation) return;
    
    try {
      await serviceAdmin.basculerStatutCompte(utilisateur.id);
      await chargerDonnees();
    } catch (err) {
      alert('Impossible de modifier le statut du compte');
      console.error(err);
    }
  };

  if (chargement) {
    return (
      <div className="page-gestion-utilisateurs">
        <div className="entete-gestion">
          <div className="icone-gestion-grande">
            <Users size={32} />
          </div>
          <div className="contenu-entete-gestion">
            <h1 className="titre-gestion">Chargement en cours...</h1>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-gestion-utilisateurs">
      
      {/* En-tête contextuel avec icône, description et bouton de création. */}
      <div className="entete-gestion">
        <div className="icone-gestion-grande">
          <Users size={32} />
        </div>
        <div className="contenu-entete-gestion">
          <h1 className="titre-gestion">Gestion des utilisateurs</h1>
          <p className="description-gestion">
            Créez, modifiez et désactivez les comptes des agents, analystes 
            et citoyens du système Tsenan'tsika.
          </p>
        </div>
        <button className="bouton-nouveau-compte" onClick={ouvrirCreation}>
          <UserPlus size={18} />
          Nouveau compte
        </button>
      </div>

      {/* Statistiques rapides par rôle. */}
      <div className="statistiques-roles">
        <div className="carte-stat-role">
          <div className="icone-stat-role role-total">
            <Users size={24} />
          </div>
          <div>
            <div className="valeur-stat-role">{statistiques.total}</div>
            <div className="label-stat-role">Total</div>
          </div>
        </div>
        <div className="carte-stat-role">
          <div className="icone-stat-role role-agent">
            <UserCheck size={24} />
          </div>
          <div>
            <div className="valeur-stat-role">{statistiques.agent}</div>
            <div className="label-stat-role">Agents</div>
          </div>
        </div>
        <div className="carte-stat-role">
          <div className="icone-stat-role role-analyste">
            <UserCheck size={24} />
          </div>
          <div>
            <div className="valeur-stat-role">{statistiques.analyste}</div>
            <div className="label-stat-role">Analystes</div>
          </div>
        </div>
        <div className="carte-stat-role">
          <div className="icone-stat-role role-citoyen">
            <UserCheck size={24} />
          </div>
          <div>
            <div className="valeur-stat-role">{statistiques.citoyen}</div>
            <div className="label-stat-role">Citoyens</div>
          </div>
        </div>
      </div>

      {/* Zone de recherche et de filtrage. */}
      <div className="barre-recherche-filtres">
        <div className="conteneur-recherche">
          <Search size={18} className="icone-recherche" />
          <input
            type="text"
            className="input-recherche"
            placeholder="Rechercher par nom, prénom ou email..."
            value={recherche}
            onChange={(e) => setRecherche(e.target.value)}
          />
        </div>
        <select
          className="select-filtre"
          value={filtreRole}
          onChange={(e) => setFiltreRole(e.target.value)}
        >
          <option value="">Tous les rôles</option>
          <option value="agent">Agents</option>
          <option value="analyste">Analystes</option>
          <option value="citoyen">Citoyens</option>
        </select>
      </div>

      {/* Tableau des utilisateurs avec design moderne. */}
      <div className="carte-tableau-utilisateurs">
        {erreur && (
          <div className="message-erreur-modal" style={{ margin: 'var(--espace-md)' }}>
            <AlertCircle size={18} />
            {erreur}
          </div>
        )}
        
        {utilisateursFiltres.length === 0 ? (
          <div className="message-liste-vide">
            <div className="icone-liste-vide">
              <Users size={32} />
            </div>
            <div>Aucun utilisateur ne correspond aux critères de recherche.</div>
          </div>
        ) : (
          <table className="tableau-utilisateurs-moderne">
            <thead>
              <tr>
                <th>Utilisateur</th>
                <th>Rôle</th>
                <th>Ville assignée</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {utilisateursFiltres.map((utilisateur) => (
                <tr key={utilisateur.id}>
                  <td>
                    <div className="nom-utilisateur-cellule">
                      <div className="avatar-cellule">
                        {obtenirInitiales(utilisateur.prenoms, utilisateur.nom)}
                      </div>
                      <div>
                        <div className="nom-complet-cellule">
                          {utilisateur.prenoms} {utilisateur.nom}
                        </div>
                        <div className="email-cellule">{utilisateur.email}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className={`badge-role-cellule role-${utilisateur.role}`}>
                      {utilisateur.role}
                    </span>
                  </td>
                  <td>{utilisateur.ville_assignee_nom || '—'}</td>
                  <td>
                    {utilisateur.statut_compte ? (
                      <span className="statut-compte-cellule actif">
                        <CheckCircle2 size={16} />
                        Actif
                      </span>
                    ) : (
                      <span className="statut-compte-cellule desactive">
                        <XCircle size={16} />
                        Désactivé
                      </span>
                    )}
                  </td>
                  <td>
                    <div className="actions-cellule">
                      <button
                        className="bouton-action"
                        onClick={() => ouvrirModification(utilisateur)}
                        title="Modifier les informations"
                      >
                        <Edit2 size={16} />
                      </button>
                      <button
                        className={`bouton-action ${utilisateur.statut_compte ? 'action-desactiver' : 'action-activer'}`}
                        onClick={() => basculerStatut(utilisateur)}
                        title={utilisateur.statut_compte ? 'Désactiver le compte' : 'Activer le compte'}
                      >
                        <Power size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal de création modification d'utilisateur. */}
      {modalOuvert && (
        <div className="fond-modal" onClick={() => setModalOuvert(false)}>
          <div className="contenu-modal" onClick={(e) => e.stopPropagation()}>
            
            <div className="entete-modal">
              <h2 className="titre-modal">
                {utilisateurEnModification ? 'Modifier le compte' : 'Nouveau compte'}
              </h2>
              <button 
                className="bouton-fermer-modal" 
                onClick={() => setModalOuvert(false)}
                type="button"
              >
                <X size={20} />
              </button>
            </div>

            {erreurFormulaire && (
              <div className="message-erreur-modal">
                <AlertCircle size={18} />
                {erreurFormulaire}
              </div>
            )}

            <form onSubmit={soumettreFormulaire}>
              
              <div className="grille-champs-modal">
                <div className="champ-modal">
                  <label className="label-modal">Nom</label>
                  <input
                    type="text"
                    className="input-modal"
                    value={formulaire.nom}
                    onChange={(e) => setFormulaire({ ...formulaire, nom: e.target.value })}
                    required
                    minLength={2}
                  />
                </div>
                <div className="champ-modal">
                  <label className="label-modal">Prénoms</label>
                  <input
                    type="text"
                    className="input-modal"
                    value={formulaire.prenoms}
                    onChange={(e) => setFormulaire({ ...formulaire, prenoms: e.target.value })}
                    required
                    minLength={2}
                  />
                </div>
              </div>

              <div className="champ-modal">
                <label className="label-modal">Email</label>
                <input
                  type="email"
                  className="input-modal"
                  value={formulaire.email}
                  onChange={(e) => setFormulaire({ ...formulaire, email: e.target.value })}
                  required
                />
              </div>

              <div className="champ-modal">
                <label className="label-modal">
                  Mot de passe
                  {utilisateurEnModification && ' (laisser vide pour ne pas modifier)'}
                </label>
                <input
                  type="password"
                  className="input-modal"
                  value={formulaire.mot_de_passe}
                  onChange={(e) => setFormulaire({ ...formulaire, mot_de_passe: e.target.value })}
                  required={!utilisateurEnModification}
                  minLength={8}
                />
                {!utilisateurEnModification && (
                  <p className="aide-modal">Minimum 8 caractères</p>
                )}
              </div>

              <div className="grille-champs-modal">
                <div className="champ-modal">
                  <label className="label-modal">Rôle</label>
                  <select
                    className="select-modal"
                    value={formulaire.role}
                    onChange={(e) => setFormulaire({ ...formulaire, role: e.target.value, ville_assignee_id: '' })}
                    required
                  >
                    <option value="agent">Agent de collecte</option>
                    <option value="analyste">Analyste</option>
                    <option value="citoyen">Citoyen</option>
                  </select>
                </div>
                {formulaire.role === 'agent' && (
                  <div className="champ-modal">
                    <label className="label-modal">Ville assignée</label>
                    <select
                      className="select-modal"
                      value={formulaire.ville_assignee_id}
                      onChange={(e) => setFormulaire({ ...formulaire, ville_assignee_id: e.target.value })}
                      required
                    >
                      <option value="">Sélectionner une ville</option>
                      {villes.filter(v => 
                        ['Antananarivo', 'Toamasina', 'Antsirabe', 'Mahajanga', 'Fianarantsoa', 'Toliara', 'Antsiranana'].includes(v.nom)
                      ).map(v => (
                        <option key={v.id} value={v.id}>{v.nom}</option>
                      ))}
                    </select>
                  </div>
                )}
              </div>

              <div className="actions-modal">
                <button
                  type="button"
                  className="bouton-annuler-modal"
                  onClick={() => setModalOuvert(false)}
                  disabled={soumissionFormulaire}
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="bouton-confirmer-modal"
                  disabled={soumissionFormulaire}
                >
                  <Save size={16} />
                  {soumissionFormulaire ? 'Enregistrement...' : 'Enregistrer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default PageGestionUtilisateurs;