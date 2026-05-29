import { useState, useEffect } from 'react';
import {
  PlusCircle, Package, MapPin, DollarSign, User, Send,
  CheckCircle2, XCircle, AlertTriangle, TrendingUp
} from 'lucide-react';
import { servicePrix, serviceSaisie, serviceAuth } from '../services/api';
import '../styles/PageSaisiePrix.css';

function PageSaisiePrix() {
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  
  const [produits, setProduits] = useState([]);
  const [villes, setVilles] = useState([]);
  
  const [produitId, setProduitId] = useState('');
  const [produitSelectionne, setProduitSelectionne] = useState(null);
  const [villeId, setVilleId] = useState('');
  const [prix, setPrix] = useState('');
  
  const [resultat, setResultat] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [soumission, setSoumission] = useState(false);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
  const chargerDonneesInitiales = async () => {
    try {
      const [produitsCharges, villesChargees] = await Promise.all([
        servicePrix.listerProduits(),
        servicePrix.listerVilles()
      ]);
      setProduits(produitsCharges);
      setVilles(villesChargees);
      
      if (utilisateur?.ville_assignee_id) {
        setVilleId(utilisateur.ville_assignee_id.toString());
      }
      
      setErreur(null);
    } catch (err) {
      setErreur('Impossible de charger les données du formulaire.');
      console.error('Erreur lors du chargement initial:', err);
    } finally {
      setChargement(false);
    }
  };
    chargerDonneesInitiales();
  }, []);

  const gererSoumission = async (evenement) => {
    evenement.preventDefault();
    
    if (!produitId || !villeId || !prix) {
      setErreur('Veuillez remplir tous les champs du formulaire.');
      return;
    }
    
    setSoumission(true);
    setErreur(null);
    setResultat(null);
    
    try {
      const reponse = await serviceSaisie.saisirPrix(
        parseInt(produitId),
        parseInt(villeId),
        parseFloat(prix),
        utilisateur.id
      );
      setResultat(reponse);
      
      if (reponse.succes && !reponse.doublon_detecte) {
        setPrix('');
      }
    } catch (err) {
      setErreur('Une erreur est survenue lors de la soumission du prix.');
      console.error('Erreur de soumission:', err);
    } finally {
      setSoumission(false);
    }
  };

  const obtenirTypeCarteResultat = () => {
    if (!resultat) return null;
    if (resultat.doublon_detecte) return 'doublon';
    if (resultat.alerte_declenchee) return 'alerte';
    return 'succes';
  };

  if (chargement) {
    return (
      <div className="page-saisie">
        <div className="entete-saisie">
          <div className="icone-saisie-grande">
            <PlusCircle size={32} />
          </div>
          <div className="contenu-entete-saisie">
            <h1 className="titre-saisie">Chargement en cours...</h1>
          </div>
        </div>
      </div>
    );
  }

  const typeCarte = obtenirTypeCarteResultat();

  return (
    <div className="page-saisie">
      
      {/* En-tête contextuel avec présentation de la fonctionnalité. */}
      <div className="entete-saisie">
        <div className="icone-saisie-grande">
          <PlusCircle size={32} />
        </div>
        <div className="contenu-entete-saisie">
          <h1 className="titre-saisie">Saisie d'un nouveau prix</h1>
          <p className="description-saisie">
            Bonjour {utilisateur?.prenoms}, soumettez ici les prix observés 
            sur les marchés. Le système vérifie automatiquement les doublons 
            et calcule les variations pour détecter les anomalies.
          </p>
        </div>
      </div>

      {/* Carte principale contenant le formulaire de saisie. */}
      <div className="carte-formulaire-saisie">
        <h2 className="titre-formulaire-saisie">Informations du prix observé</h2>
        
        {erreur && (
          <div className="message-erreur-auth" style={{ marginBottom: 'var(--espace-md)' }}>
            <XCircle size={18} />
            <span>{erreur}</span>
          </div>
        )}
        
        <form onSubmit={gererSoumission}>
          
          <div className="grille-champs">
            <div className="groupe-champ-moderne">
              <label className="label-champ-moderne" htmlFor="produit">
                Produit observé
              </label>
              <div className="conteneur-input-moderne">
                <Package size={18} className="icone-input-moderne" />
                <select
                  id="produit"
                  className="select-saisie"
                  value={produitId}
                  onChange={(e) => {
                    const nouvelId = e.target.value;
                    setProduitId(nouvelId);
                    const produit = produits.find(p => p.id === parseInt(nouvelId));
                    setProduitSelectionne(produit || null);
                  }}
                  disabled={soumission}
                  required
                >
                  <option value="">Sélectionner un produit</option>
                  {produits.map((produit) => (
                    <option key={produit.id} value={produit.id}>
                      {produit.nom_fr} ({produit.nom_mg})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="groupe-champ-moderne">
              <label className="label-champ-moderne">
                Votre ville d'affectation
              </label>
              <div className="affichage-ville-assignee">
                <MapPin size={20} />
                <span className="nom-ville-assignee">
                  {utilisateur?.ville_assignee_nom || 'Aucune ville assignée'}
                </span>
                <span className="badge-affectation">Affecté</span>
              </div>
              <p className="aide-champ">
                Conformément à votre affectation administrative, vous pouvez saisir 
                uniquement les prix observés dans cette ville.
              </p>
            </div>
          </div>

          <div className="groupe-champ-moderne">
            <label className="label-champ-moderne" htmlFor="prix">
              {produitSelectionne 
                ? `Prix par ${produitSelectionne.unite} en Ariary`
                : 'Prix observé en Ariary'}
            </label>
            <div className="conteneur-input-moderne">
              <DollarSign size={18} className="icone-input-moderne" />
              <input
                id="prix"
                type="number"
                className="input-saisie"
                placeholder="Exemple : 3500"
                value={prix}
                onChange={(e) => setPrix(e.target.value)}
                disabled={soumission}
                min="0"
                step="0.01"
                required
              />
            </div>
            <p className="aide-champ">
              {produitSelectionne
                ? `Saisissez le prix d'un ${produitSelectionne.unite} de ${produitSelectionne.nom_fr.toLowerCase()} observé sur le marché.`
                : 'Sélectionnez d\'abord un produit pour voir l\'unité de mesure attendue.'}
            </p>
          </div>

          <button type="submit" className="bouton-soumettre" disabled={soumission}>
            {soumission ? (
              <>
                <span className="spinner-saisie"></span>
                Traitement en cours...
              </>
            ) : (
              <>
                <Send size={18} />
                Soumettre le prix
              </>
            )}
          </button>
        </form>
      </div>

      {/* Carte de résultat affichée dynamiquement après chaque soumission. */}
      {resultat && (
        <div className={`carte-resultat carte-resultat-${typeCarte}`}>
          
          {typeCarte === 'doublon' && (
            <>
              <div className="entete-resultat">
                <XCircle size={24} />
                Doublon détecté
              </div>
              <div className="message-resultat">
                {resultat.message} L'algorithme Rabin-Karp a identifié que ce prix 
                a déjà été soumis dans les dernières 24 heures.
              </div>
            </>
          )}
          
          {typeCarte === 'succes' && (
            <>
              <div className="entete-resultat">
                <CheckCircle2 size={24} />
                Prix enregistré avec succès
              </div>
              <div className="message-resultat">
                Le prix a été validé et ajouté à la base de données. Aucune 
                anomalie significative n'a été détectée par rapport à la moyenne récente.
              </div>
            </>
          )}
          
          {typeCarte === 'alerte' && (
            <>
              <div className="entete-resultat">
                <AlertTriangle size={24} />
                Prix enregistré avec alerte
              </div>
              <div className="message-resultat">
                Le prix a été validé mais sa variation par rapport à la moyenne récente 
                dépasse le seuil de 20%. Une alerte a été automatiquement déclenchée.
              </div>
            </>
          )}
          
          {(resultat.rapport_id || resultat.prix_marche_id) && (
            <div className="details-resultat">
              <div className="titre-details">Détails du traitement</div>
              <ul className="liste-details">
                {resultat.rapport_id && (
                  <li className="element-detail">
                    <span>Identifiant du rapport</span>
                    <span className="valeur-detail">#{resultat.rapport_id}</span>
                  </li>
                )}
                {resultat.prix_marche_id && (
                  <li className="element-detail">
                    <span>Identifiant du prix marché</span>
                    <span className="valeur-detail">#{resultat.prix_marche_id}</span>
                  </li>
                )}
                {resultat.variation_pourcent !== null && resultat.variation_pourcent !== undefined && (
                  <li className="element-detail">
                    <span>Variation par rapport à la moyenne</span>
                    <span className={`valeur-detail ${resultat.variation_pourcent > 0 ? 'valeur-variation-positive' : 'valeur-variation-negative'}`}>
                      {resultat.variation_pourcent > 0 ? '+' : ''}{resultat.variation_pourcent}%
                    </span>
                  </li>
                )}
              </ul>
            </div>
          )}
          
          {resultat.alerte_declenchee && (
            <div className="bandeau-alerte-declenchee">
              <TrendingUp size={18} />
              Cette anomalie est maintenant visible sur le tableau de bord.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default PageSaisiePrix;