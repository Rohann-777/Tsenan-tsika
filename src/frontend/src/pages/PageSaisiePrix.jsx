// Page de saisie de prix de Tsenan'tsika.
// Cette page permet aux agents de collecte de soumettre les prix qu'ils
// observent sur les marchés locaux. Elle déclenche tout le pipeline de
// traitement backend incluant la détection de doublons par Rabin-Karp
// et la mise à jour du Top-k qui peut générer une alerte.

import { useState, useEffect } from 'react';
import { servicePrix, serviceSaisie } from '../services/api';

function PageSaisiePrix() {
  // Listes des produits et villes récupérées depuis l'API pour alimenter
  // les menus déroulants du formulaire. Elles sont chargées une seule
  // fois au démarrage de la page pour éviter des appels répétés.
  const [produits, setProduits] = useState([]);
  const [villes, setVilles] = useState([]);
  
  // Valeurs actuellement saisies par l'utilisateur dans le formulaire.
  // Ces états sont mis à jour à chaque modification d'un champ et
  // serviront à construire le corps de la requête lors de la soumission.
  const [produitId, setProduitId] = useState('');
  const [villeId, setVilleId] = useState('');
  const [prix, setPrix] = useState('');
  const [agentId, setAgentId] = useState('4');
  
  // Résultat retourné par le backend après traitement de la saisie.
  // Contient les informations sur le succès ou l'échec de l'opération
  // ainsi que les détails comme la variation de prix calculée.
  const [resultat, setResultat] = useState(null);
  
  // États pour la gestion du chargement initial et de la soumission.
  // Ils permettent d'afficher des indicateurs visuels appropriés à
  // chaque étape du cycle de vie du formulaire.
  const [chargement, setChargement] = useState(true);
  const [soumission, setSoumission] = useState(false);
  const [erreur, setErreur] = useState(null);

  // Chargement initial des produits et des villes au montage du composant.
  // Ces deux requêtes sont lancées en parallèle pour optimiser le temps
  // de chargement de la page.
  useEffect(() => {
    const chargerDonneesInitiales = async () => {
      try {
        const [produitsCharges, villesChargees] = await Promise.all([
          servicePrix.listerProduits(),
          servicePrix.listerVilles()
        ]);
        setProduits(produitsCharges);
        setVilles(villesChargees);
        setErreur(null);
      } catch (err) {
        setErreur('Impossible de charger les données du formulaire. Vérifiez que le serveur backend est démarré.');
        console.error('Erreur lors du chargement initial:', err);
      } finally {
        setChargement(false);
      }
    };

    chargerDonneesInitiales();
  }, []);

  // Gestionnaire de soumission du formulaire qui envoie les données au
  // backend et affiche le résultat retourné. Cette fonction est appelée
  // quand l'utilisateur clique sur le bouton de soumission.
  const gererSoumission = async (evenement) => {
    // Empêche le rechargement de la page qui est le comportement par
    // défaut d'un formulaire HTML lors de la soumission.
    evenement.preventDefault();
    
    // Validation côté client avant l'envoi pour éviter des appels API
    // inutiles avec des données incomplètes.
    if (!produitId || !villeId || !prix || !agentId) {
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
        parseInt(agentId)
      );
      setResultat(reponse);
      
      // Si la saisie a réussi, on vide les champs pour faciliter une
      // nouvelle saisie. Si un doublon a été détecté, on garde les
      // valeurs pour que l'utilisateur puisse les modifier facilement.
      if (reponse.succes) {
        setPrix('');
      }
    } catch (err) {
      setErreur('Une erreur est survenue lors de la soumission du prix.');
      console.error('Erreur de soumission:', err);
    } finally {
      setSoumission(false);
    }
  };

  // Affichage du message de chargement initial.
  if (chargement) {
    return (
      <div className="carte">
        <h2>Saisie de prix</h2>
        <div className="message-info">
          Chargement du formulaire en cours...
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Section d'introduction qui explique le rôle de cette page
          et donne le contexte aux agents de collecte qui vont l'utiliser. */}
      <div className="carte">
        <h2>Saisie d'un nouveau prix</h2>
        <p>
          Cette interface permet aux agents de collecte de soumettre les
          prix observés sur les marchés locaux. Chaque saisie est automatiquement
          vérifiée pour détecter les doublons éventuels, puis le système calcule
          la variation par rapport à la moyenne récente du produit dans la
          ville concernée. Si la variation dépasse 20%, une alerte
          est immédiatement déclenchée pour signaler une anomalie potentielle.
        </p>
      </div>

      {/* Formulaire principal de saisie avec ses différents champs.
          Chaque champ utilise l'état React pour stocker sa valeur et
          mettre à jour le composant à chaque modification. */}
      <div className="carte">
        <h2>Formulaire de saisie</h2>
        
        {erreur && (
          <div className="message-erreur">
            {erreur}
          </div>
        )}
        
        <form onSubmit={gererSoumission}>
          
          <div className="champ-formulaire">
            <label htmlFor="produit">Produit observé</label>
            <select
              id="produit"
              value={produitId}
              onChange={(e) => setProduitId(e.target.value)}
              disabled={soumission}
            >
              <option value="">-- Sélectionner un produit --</option>
              {produits.map((produit) => (
                <option key={produit.id} value={produit.id}>
                  {produit.nom_fr} ({produit.nom_mg}) - en {produit.unite}
                </option>
              ))}
            </select>
          </div>

          <div className="champ-formulaire">
            <label htmlFor="ville">Ville d'observation</label>
            <select
              id="ville"
              value={villeId}
              onChange={(e) => setVilleId(e.target.value)}
              disabled={soumission}
            >
              <option value="">-- Sélectionner une ville --</option>
              {villes.map((ville) => (
                <option key={ville.id} value={ville.id}>
                  {ville.nom} ({ville.region})
                </option>
              ))}
            </select>
          </div>

          <div className="champ-formulaire">
            <label htmlFor="prix">Prix observé en Ariary</label>
            <input
              type="number"
              id="prix"
              value={prix}
              onChange={(e) => setPrix(e.target.value)}
              placeholder="Exemple : 3500"
              min="0"
              step="0.01"
              disabled={soumission}
            />
          </div>

          <div className="champ-formulaire">
            <label htmlFor="agent">Identifiant de l'agent</label>
            <input
              type="number"
              id="agent"
              value={agentId}
              onChange={(e) => setAgentId(e.target.value)}
              placeholder="Votre identifiant agent"
              min="1"
              disabled={soumission}
            />
            <small style={{ color: '#757575', display: 'block', marginTop: '0.25rem' }}>
              Par défaut, l'identifiant 4 correspond à l'agent Sophie utilisé pour les tests.
            </small>
          </div>

          <button type="submit" className="bouton" disabled={soumission}>
            {soumission ? 'Soumission en cours...' : 'Soumettre le prix'}
          </button>
          
        </form>
      </div>

      {/* Affichage du résultat de la soumission avec un style différent
          selon que l'opération a réussi, qu'un doublon a été détecté,
          ou qu'une alerte a été déclenchée. */}
      {resultat && (
        <div className="carte">
          <h2>Résultat de la soumission</h2>
          
          {resultat.doublon_detecte && (
            <div className="message-erreur">
              <strong>Doublon détecté</strong>
              <p style={{ marginTop: '0.5rem' }}>
                {resultat.message}
              </p>
            </div>
          )}
          
          {resultat.succes && !resultat.doublon_detecte && (
            <div className="message-succes">
              <strong>Prix enregistré avec succès</strong>
              <p style={{ marginTop: '0.5rem' }}>
                Le prix a été validé et ajouté à la base de données.
              </p>
            </div>
          )}
          
          {/* Affichage des détails techniques pour information.
              Ces informations sont utiles pour démontrer le fonctionnement
              du système lors de la soutenance. */}
          <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#f5f5f0', borderRadius: '4px' }}>
            <p><strong>Détails du traitement :</strong></p>
            <ul style={{ marginTop: '0.5rem', listStyle: 'none' }}>
              {resultat.rapport_id && (
                <li>Identifiant du rapport en base : {resultat.rapport_id}</li>
              )}
              {resultat.prix_marche_id && (
                <li>Identifiant du prix marché en base : {resultat.prix_marche_id}</li>
              )}
              {resultat.variation_pourcent !== null && resultat.variation_pourcent !== undefined && (
                <li>
                  Variation par rapport à la moyenne récente :{' '}
                  <strong style={{ color: resultat.variation_pourcent > 0 ? '#c62828' : '#2e7d32' }}>
                    {resultat.variation_pourcent > 0 ? '+' : ''}{resultat.variation_pourcent}%
                  </strong>
                </li>
              )}
              {resultat.alerte_declenchee && (
                <li style={{ marginTop: '0.5rem', color: '#c62828' }}>
                  <strong>Une alerte a été automatiquement déclenchée</strong> car la variation dépasse le seuil de 20 pour cent.
                </li>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default PageSaisiePrix;