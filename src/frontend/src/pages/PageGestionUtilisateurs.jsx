// Page de gestion des utilisateurs pour l'administrateur de Tsenan'tsika.
// Cette page permet de visualiser, créer, modifier et désactiver les
// comptes des agents, analystes et citoyens du système. Les comptes
// administrateurs sont hors du périmètre de gestion conformément à
// notre décision architecturale.

import { useState, useEffect } from 'react';
import { 
  Users, UserPlus, Edit2, Power, Search, Filter,
  CheckCircle2, XCircle, AlertCircle, X, Save
} from 'lucide-react';
import { serviceAdmin, servicePrix } from '../services/api';

function PageGestionUtilisateurs() {
  // États pour gérer les données affichées sur la page
  const [utilisateurs, setUtilisateurs] = useState([]);
  const [villes, setVilles] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);
  
  // États pour le filtrage et la recherche
  const [filtreRole, setFiltreRole] = useState('');
  const [recherche, setRecherche] = useState('');
  
  // États pour le formulaire de création/modification
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

  // Chargement initial des données au montage du composant
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
      setErreur('Impossible de charger les utilisateurs');
      console.error(err);
    } finally {
      setChargement(false);
    }
  };

  // Filtrage des utilisateurs selon les critères de recherche
  const utilisateursFiltres = utilisateurs.filter(u => {
    const correspondRole = !filtreRole || u.role === filtreRole;
    const correspondRecherche = !recherche || 
      u.nom.toLowerCase().includes(recherche.toLowerCase()) ||
      u.prenoms.toLowerCase().includes(recherche.toLowerCase()) ||
      u.email.toLowerCase().includes(recherche.toLowerCase());
    return correspondRole && correspondRecherche;
  });

  // Ouverture du modal en mode création avec formulaire vide
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

  // Ouverture du modal en mode modification avec données pré-remplies
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

  // Soumission du formulaire pour création ou modification
  const soumettreFormulaire = async (e) => {
    e.preventDefault();
    setErreurFormulaire(null);
    setSoumissionFormulaire(true);
    
    try {
      const donnees = {
        nom: formulaire.nom,
        prenoms: formulaire.prenoms,
        email: formulaire.email,
        role: formulaire.role,
        ville_assignee_id: formulaire.role === 'agent' 
          ? parseInt(formulaire.ville_assignee_id) || null 
          : null
      };
      
      if (formulaire.mot_de_passe) {
        donnees.mot_de_passe = formulaire.mot_de_passe;
      }
      
      if (utilisateurEnModification) {
        await serviceAdmin.modifierUtilisateur(
          utilisateurEnModification.id, 
          donnees
        );
      } else {
        if (!formulaire.mot_de_passe) {
          setErreurFormulaire('Le mot de passe est obligatoire pour un nouveau compte');
          setSoumissionFormulaire(false);
          return;
        }
        donnees.mot_de_passe = formulaire.mot_de_passe;
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

  // Basculement du statut actif/désactivé d'un compte
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

  // Détermination de la couleur du badge selon le rôle
  const obtenirCouleurRole = (role) => {
    if (role === 'agent') return { bg: '#fef3c7', texte: '#92400e' };
    if (role === 'analyste') return { bg: '#dbeafe', texte: '#1e40af' };
    if (role === 'citoyen') return { bg: '#d1fae5', texte: '#065f46' };
    return { bg: '#f3f4f6', texte: '#374151' };
  };

  if (chargement) {
    return (
      <div className="carte">
        <h2>Gestion des utilisateurs</h2>
        <div className="message-info">Chargement en cours...</div>
      </div>
    );
  }

  return (
    <div>
      {/* Carte d'en-tête avec titre et bouton de création */}
      <div className="carte">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Users size={28} />
              Gestion des utilisateurs
            </h2>
            <p style={{ color: '#6b7280', marginTop: '0.5rem' }}>
              Créez, modifiez ou désactivez les comptes des agents, analystes et citoyens du système.
            </p>
          </div>
          <button
            className="bouton"
            onClick={ouvrirCreation}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <UserPlus size={18} />
            Nouveau compte
          </button>
        </div>
      </div>

      {/* Carte de filtrage et recherche */}
      <div className="carte">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 200px', gap: '1rem' }}>
          <div className="conteneur-input" style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#9ca3af' }} />
            <input
              type="text"
              placeholder="Rechercher par nom, prénom ou email..."
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
            value={filtreRole}
            onChange={(e) => setFiltreRole(e.target.value)}
            style={{
              padding: '0.75rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.375rem',
              fontSize: '0.95rem'
            }}
          >
            <option value="">Tous les rôles</option>
            <option value="agent">Agents</option>
            <option value="analyste">Analystes</option>
            <option value="citoyen">Citoyens</option>
          </select>
        </div>
      </div>

      {/* Carte avec la liste des utilisateurs */}
      <div className="carte">
        {erreur && <div className="message-erreur">{erreur}</div>}
        
        {utilisateursFiltres.length === 0 ? (
          <div className="message-info">
            Aucun utilisateur ne correspond aux critères de recherche.
          </div>
        ) : (
          <table className="tableau-donnees">
            <thead>
              <tr>
                <th>Utilisateur</th>
                <th>Email</th>
                <th>Rôle</th>
                <th>Ville assignée</th>
                <th>Statut</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {utilisateursFiltres.map((utilisateur) => {
                const couleurs = obtenirCouleurRole(utilisateur.role);
                return (
                  <tr key={utilisateur.id}>
                    <td>
                      <strong>{utilisateur.prenoms} {utilisateur.nom}</strong>
                    </td>
                    <td>{utilisateur.email}</td>
                    <td>
                      <span style={{
                        padding: '0.25rem 0.75rem',
                        backgroundColor: couleurs.bg,
                        color: couleurs.texte,
                        borderRadius: '9999px',
                        fontSize: '0.85rem',
                        fontWeight: '600',
                        textTransform: 'capitalize'
                      }}>
                        {utilisateur.role}
                      </span>
                    </td>
                    <td>{utilisateur.ville_assignee_nom || '—'}</td>
                    <td>
                      {utilisateur.statut_compte ? (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#059669' }}>
                          <CheckCircle2 size={16} />
                          Actif
                        </span>
                      ) : (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#dc2626' }}>
                          <XCircle size={16} />
                          Désactivé
                        </span>
                      )}
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <button
                        onClick={() => ouvrirModification(utilisateur)}
                        title="Modifier"
                        style={{
                          background: 'transparent',
                          border: 'none',
                          cursor: 'pointer',
                          padding: '0.5rem',
                          color: '#6b7280',
                          marginRight: '0.5rem'
                        }}
                      >
                        <Edit2 size={18} />
                      </button>
                      <button
                        onClick={() => basculerStatut(utilisateur)}
                        title={utilisateur.statut_compte ? 'Désactiver' : 'Activer'}
                        style={{
                          background: 'transparent',
                          border: 'none',
                          cursor: 'pointer',
                          padding: '0.5rem',
                          color: utilisateur.statut_compte ? '#dc2626' : '#059669'
                        }}
                      >
                        <Power size={18} />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal de création/modification d'utilisateur */}
      {modalOuvert && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '1rem'
          }}
          onClick={() => setModalOuvert(false)}
        >
          <div
            style={{
              backgroundColor: 'white',
              borderRadius: '0.75rem',
              padding: '2rem',
              maxWidth: '500px',
              width: '100%',
              maxHeight: '90vh',
              overflowY: 'auto'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '1.5rem', fontWeight: '700' }}>
                {utilisateurEnModification ? 'Modifier le compte' : 'Nouveau compte'}
              </h3>
              <button
                onClick={() => setModalOuvert(false)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '0.5rem',
                  color: '#6b7280'
                }}
              >
                <X size={24} />
              </button>
            </div>

            {erreurFormulaire && (
              <div className="message-erreur" style={{ marginBottom: '1rem' }}>
                <AlertCircle size={16} style={{ marginRight: '0.5rem', verticalAlign: 'middle' }} />
                {erreurFormulaire}
              </div>
            )}

            <form onSubmit={soumettreFormulaire}>
              <div className="champ-formulaire">
                <label>Nom</label>
                <input
                  type="text"
                  value={formulaire.nom}
                  onChange={(e) => setFormulaire({ ...formulaire, nom: e.target.value })}
                  required
                  minLength={2}
                />
              </div>
              <div className="champ-formulaire">
                <label>Prénoms</label>
                <input
                  type="text"
                  value={formulaire.prenoms}
                  onChange={(e) => setFormulaire({ ...formulaire, prenoms: e.target.value })}
                  required
                  minLength={2}
                />
              </div>
              <div className="champ-formulaire">
                <label>Email</label>
                <input
                  type="email"
                  value={formulaire.email}
                  onChange={(e) => setFormulaire({ ...formulaire, email: e.target.value })}
                  required
                />
              </div>
              <div className="champ-formulaire">
                <label>
                  Mot de passe 
                  {utilisateurEnModification && (
                    <span style={{ fontWeight: 'normal', color: '#6b7280', fontSize: '0.85rem' }}>
                      {' '}(laissez vide pour ne pas modifier)
                    </span>
                  )}
                </label>
                <input
                  type="password"
                  value={formulaire.mot_de_passe}
                  onChange={(e) => setFormulaire({ ...formulaire, mot_de_passe: e.target.value })}
                  required={!utilisateurEnModification}
                  minLength={8}
                />
              </div>
              <div className="champ-formulaire">
                <label>Rôle</label>
                <select
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
                <div className="champ-formulaire">
                  <label>Ville assignée</label>
                  <select
                    value={formulaire.ville_assignee_id}
                    onChange={(e) => setFormulaire({ ...formulaire, ville_assignee_id: e.target.value })}
                    required
                  >
                    <option value="">Sélectionner une ville</option>
                    {villes.map(v => (
                      <option key={v.id} value={v.id}>{v.nom}</option>
                    ))}
                  </select>
                </div>
              )}

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                <button
                  type="button"
                  onClick={() => setModalOuvert(false)}
                  disabled={soumissionFormulaire}
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: 'white',
                    color: '#374151',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                    cursor: 'pointer',
                    fontWeight: '500'
                  }}
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  disabled={soumissionFormulaire}
                  className="bouton"
                  style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
                >
                  <Save size={18} />
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