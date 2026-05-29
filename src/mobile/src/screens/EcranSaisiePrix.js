import React, { useState, useEffect } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  SafeAreaView, ScrollView, KeyboardAvoidingView, Platform,
  ActivityIndicator, Alert, StatusBar, Modal
} from 'react-native';
import {
  PlusCircle, Package, MapPin, DollarSign, Send,
  CheckCircle2, XCircle, AlertTriangle, TrendingUp,
  ChevronDown, X
} from 'lucide-react-native';
import { servicePrix, serviceSaisie } from '../services/api';
import { utiliserAuth } from '../contexts/ContexteAuth';
import { couleurs, espacements, rayons, tailles } from '../styles/theme';

export default function EcranSaisiePrix() {
  const { utilisateur } = utiliserAuth();
  
  const [produits, setProduits] = useState([]);
  const [produitId, setProduitId] = useState(null);
  const [produitSelectionne, setProduitSelectionne] = useState(null);
  const [prix, setPrix] = useState('');
  
  const [resultat, setResultat] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [soumission, setSoumission] = useState(false);
  const [erreur, setErreur] = useState(null);
  const [modalProduitOuvert, setModalProduitOuvert] = useState(false);

  useEffect(() => {
    const chargerProduits = async () => {
      try {
        const produitsCharges = await servicePrix.listerProduits();
        setProduits(produitsCharges);
        setErreur(null);
      } catch (err) {
        setErreur('Impossible de charger les produits');
        console.error('Erreur de chargement:', err);
      } finally {
        setChargement(false);
      }
    };
    chargerProduits();
  }, []);

  const gererSoumission = async () => {
    if (!produitId || !prix) {
      Alert.alert('Champs manquants', 'Veuillez sélectionner un produit et saisir un prix.');
      return;
    }

    if (!utilisateur?.ville_assignee_id) {
      Alert.alert('Erreur', 'Aucune ville assignée à votre compte.');
      return;
    }

    setSoumission(true);
    setErreur(null);
    setResultat(null);

    try {
      const reponse = await serviceSaisie.saisirPrix(
        produitId,
        utilisateur.ville_assignee_id,
        parseFloat(prix),
        utilisateur.id
      );
      setResultat(reponse);

      // Si succès sans doublon, on vide le prix pour faciliter la saisie suivante.
      if (reponse.succes && !reponse.doublon_detecte) {
        setPrix('');
      }
    } catch (err) {
      Alert.alert('Erreur', 'Impossible de soumettre le prix.');
      console.error('Erreur de soumission:', err);
    } finally {
      setSoumission(false);
    }
  };

  const selectionnerProduit = (produit) => {
    setProduitId(produit.id);
    setProduitSelectionne(produit);
    setModalProduitOuvert(false);
    setResultat(null);
  };

  const obtenirTypeResultat = () => {
    if (!resultat) return null;
    if (resultat.doublon_detecte) return 'doublon';
    if (resultat.alerte_declenchee) return 'alerte';
    return 'succes';
  };

  if (chargement) {
    return (
      <SafeAreaView style={styles.conteneurChargement}>
        <ActivityIndicator size="large" color={couleurs.secondaire} />
        <Text style={styles.texteChargement}>Chargement en cours...</Text>
      </SafeAreaView>
    );
  }

  const typeResultat = obtenirTypeResultat();

  return (
    <SafeAreaView style={styles.conteneur}>
      <StatusBar barStyle="light-content" backgroundColor={couleurs.secondaireFoncee} />

      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.kav}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          
          {/* En-tête contextuel avec présentation de l'écran. */}
          <View style={styles.entete}>
            <View style={styles.entetTitreSection}>
              <PlusCircle size={28} color={couleurs.texteInverse} />
              <Text style={styles.titreEntete}>Saisie de prix</Text>
            </View>
            <Text style={styles.descriptionEntete}>
              Bonjour {utilisateur?.prenoms}, soumettez les prix observés sur le marché.
            </Text>
          </View>

          {erreur && (
            <View style={styles.boiteErreur}>
              <XCircle size={18} color={couleurs.erreurTexte} />
              <Text style={styles.texteErreur}>{erreur}</Text>
            </View>
          )}

          {/* Carte du formulaire de saisie. */}
          <View style={styles.carteFormulaire}>
            <Text style={styles.titreFormulaire}>Informations du prix</Text>

            {/* Ville assignée en lecture seule. */}
            <View style={styles.groupeChamp}>
              <Text style={styles.label}>Votre ville d'affectation</Text>
              <View style={styles.affichageVille}>
                <MapPin size={20} color={couleurs.secondaireFoncee} />
                <Text style={styles.texteVille}>
                  {utilisateur?.ville_assignee_nom || 'Aucune ville assignée'}
                </Text>
                <View style={styles.badgeAffectation}>
                  <Text style={styles.texteBadgeAffectation}>Affecté</Text>
                </View>
              </View>
              <Text style={styles.aideChamp}>
                Vous ne pouvez saisir que les prix de cette ville.
              </Text>
            </View>

            {/* Sélection du produit via modal pour une meilleure expérience mobile. */}
            <View style={styles.groupeChamp}>
             <Text style={styles.label}>Produit observé</Text>
                <TouchableOpacity
                style={styles.selecteurProduit}
                onPress={() => setModalProduitOuvert(true)}
                activeOpacity={0.7}
            >
                <Package size={20} color={couleurs.texteDiscret} />
                <Text style={[
                styles.texteSelecteurProduit,
                !produitSelectionne && styles.placeholderSelecteur
                ]}>
                {produitSelectionne 
                    ? `${produitSelectionne.nom_fr} (${produitSelectionne.nom_mg})`
                    : 'Sélectionner un produit'}
                </Text>
                <ChevronDown size={20} color={couleurs.texteDiscret} />
            </TouchableOpacity>
            {produitSelectionne && (
                <View style={styles.bandeauUnite}>
                <Text style={styles.texteBandeauUnite}>
                    Prix attendu par {produitSelectionne.unite}
                </Text>
                </View>
            )}
            </View>

            {/* Champ de saisie du prix avec clavier numérique. */}
            <View style={styles.groupeChamp}>
                <Text style={styles.label}>
                    {produitSelectionne 
                    ? `Prix par ${produitSelectionne.unite} en Ariary`
                    : 'Prix observé en Ariary'}
                </Text>
                <View style={styles.conteneurInputPrix}>
                    <DollarSign size={20} color={couleurs.texteDiscret} />
                    <TextInput
                    style={styles.inputPrix}
                    placeholder="Exemple : 3500"
                    placeholderTextColor={couleurs.texteDiscret}
                    value={prix}
                    onChangeText={setPrix}
                    keyboardType="numeric"
                    editable={!soumission}
                    />
                    <Text style={styles.uniteAriary}>
                    {produitSelectionne ? `Ar / ${produitSelectionne.unite}` : 'Ar'}
                    </Text>
                </View>
                <Text style={styles.aideChamp}>
                    {produitSelectionne
                    ? `Saisissez le prix d'un ${produitSelectionne.unite} de ${produitSelectionne.nom_fr.toLowerCase()} sur le marché.`
                    : 'Sélectionnez d\'abord un produit pour voir l\'unité attendue.'}
                </Text>
            </View>

            {/* Bouton de soumission. */}
            <TouchableOpacity
              style={[styles.boutonSoumettre, soumission && styles.boutonDesactive]}
              onPress={gererSoumission}
              disabled={soumission}
              activeOpacity={0.8}
            >
              {soumission ? (
                <ActivityIndicator color={couleurs.texteInverse} />
              ) : (
                <>
                  <Send size={20} color={couleurs.texteInverse} />
                  <Text style={styles.texteBoutonSoumettre}>Soumettre le prix</Text>
                </>
              )}
            </TouchableOpacity>
          </View>

          {/* Carte de résultat affichée dynamiquement. */}
          {resultat && (
            <View style={[
              styles.carteResultat,
              typeResultat === 'succes' && styles.carteResultatSucces,
              typeResultat === 'doublon' && styles.carteResultatDoublon,
              typeResultat === 'alerte' && styles.carteResultatAlerte,
            ]}>
              
              {typeResultat === 'succes' && (
                <>
                  <View style={styles.entetResultat}>
                    <CheckCircle2 size={24} color={couleurs.succes} />
                    <Text style={[styles.titreResultat, { color: couleurs.succesTexte }]}>
                      Prix enregistré
                    </Text>
                  </View>
                  <Text style={[styles.messageResultat, { color: couleurs.succesTexte }]}>
                    Le prix a été validé et ajouté à la base de données.
                  </Text>
                </>
              )}

              {typeResultat === 'doublon' && (
                <>
                  <View style={styles.entetResultat}>
                    <XCircle size={24} color={couleurs.erreur} />
                    <Text style={[styles.titreResultat, { color: couleurs.erreurTexte }]}>
                      Doublon détecté
                    </Text>
                  </View>
                  <Text style={[styles.messageResultat, { color: couleurs.erreurTexte }]}>
                    Ce prix a déjà été soumis dans les dernières 24 heures.
                  </Text>
                </>
              )}

              {typeResultat === 'alerte' && (
                <>
                  <View style={styles.entetResultat}>
                    <AlertTriangle size={24} color={couleurs.avertissement} />
                    <Text style={[styles.titreResultat, { color: couleurs.avertissementTexte }]}>
                      Alerte déclenchée
                    </Text>
                  </View>
                  <Text style={[styles.messageResultat, { color: couleurs.avertissementTexte }]}>
                    Le prix a été validé mais sa variation dépasse 20%.
                  </Text>
                  <View style={styles.bandeauAlerte}>
                    <TrendingUp size={16} color={couleurs.texteInverse} />
                    <Text style={styles.texteBandeauAlerte}>
                      Visible sur le tableau de bord
                    </Text>
                  </View>
                </>
              )}

              {resultat.variation_pourcent !== null && resultat.variation_pourcent !== undefined && (
                <View style={styles.detailsResultat}>
                  <Text style={styles.labelDetail}>Variation par rapport à la moyenne</Text>
                  <Text style={[
                    styles.valeurDetail,
                    { color: resultat.variation_pourcent > 0 ? couleurs.erreur : couleurs.succes }
                  ]}>
                    {resultat.variation_pourcent > 0 ? '+' : ''}{resultat.variation_pourcent}%
                  </Text>
                </View>
              )}
            </View>
          )}

        </ScrollView>
      </KeyboardAvoidingView>

      {/* Modal de sélection du produit. */}
      <Modal
        visible={modalProduitOuvert}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setModalProduitOuvert(false)}
      >
        <View style={styles.fondModal}>
          <View style={styles.contenuModal}>
            <View style={styles.entetModal}>
              <Text style={styles.titreModal}>Choisir un produit</Text>
              <TouchableOpacity
                onPress={() => setModalProduitOuvert(false)}
                style={styles.boutonFermerModal}
              >
                <X size={24} color={couleurs.texteDiscret} />
              </TouchableOpacity>
            </View>
            
            <ScrollView style={styles.listeProduits}>
              {produits.map((produit) => (
                <TouchableOpacity
                  key={produit.id}
                  style={[
                    styles.itemProduit,
                    produitId === produit.id && styles.itemProduitSelectionne
                  ]}
                  onPress={() => selectionnerProduit(produit)}
                  activeOpacity={0.7}
                >
                  <Package size={20} color={
                    produitId === produit.id ? couleurs.secondaire : couleurs.texteDiscret
                  } />
                  <View style={styles.infoProduit}>
                    <Text style={[
                      styles.nomProduitFr,
                      produitId === produit.id && styles.nomProduitSelectionne
                    ]}>
                      {produit.nom_fr}
                    </Text>
                    <Text style={styles.nomProduitMg}>{produit.nom_mg}</Text>
                  </View>
                  {produitId === produit.id && (
                    <CheckCircle2 size={20} color={couleurs.secondaire} />
                  )}
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  conteneur: {
    flex: 1,
    backgroundColor: couleurs.fond,
  },
  conteneurChargement: {
    flex: 1,
    backgroundColor: couleurs.fond,
    justifyContent: 'center',
    alignItems: 'center',
    gap: espacements.md,
  },
  texteChargement: {
    fontSize: tailles.texteBase,
    color: couleurs.texteDiscret,
  },
  kav: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: espacements.xl,
  },
  entete: {
    backgroundColor: couleurs.secondaire,
    paddingHorizontal: espacements.lg,
    paddingTop: espacements.lg,
    paddingBottom: espacements.xxl,
    borderBottomLeftRadius: rayons.xl,
    borderBottomRightRadius: rayons.xl,
  },
  entetTitreSection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    marginBottom: espacements.sm,
  },
  titreEntete: {
    fontSize: tailles.texteXl,
    fontWeight: '800',
    color: couleurs.texteInverse,
  },
  descriptionEntete: {
    fontSize: tailles.texteBase,
    color: 'rgba(255, 255, 255, 0.9)',
    lineHeight: 22,
  },
  boiteErreur: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    backgroundColor: couleurs.erreurFond,
    marginHorizontal: espacements.lg,
    marginTop: espacements.md,
    padding: espacements.md,
    borderRadius: rayons.md,
    borderLeftWidth: 4,
    borderLeftColor: couleurs.erreur,
  },
  texteErreur: {
    flex: 1,
    color: couleurs.erreurTexte,
    fontSize: tailles.texteSm,
  },
  carteFormulaire: {
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    marginTop: -espacements.lg,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  titreFormulaire: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
    color: couleurs.textePrincipal,
    marginBottom: espacements.lg,
    paddingBottom: espacements.sm,
    borderBottomWidth: 1,
    borderBottomColor: couleurs.bordure,
  },
  groupeChamp: {
    marginBottom: espacements.lg,
  },
  label: {
    fontSize: tailles.texteSm,
    fontWeight: '600',
    color: couleurs.texteSecondaire,
    marginBottom: espacements.sm,
  },
  affichageVille: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    padding: espacements.md,
    backgroundColor: couleurs.secondaireTresClaire,
    borderWidth: 2,
    borderColor: couleurs.secondaire,
    borderRadius: rayons.md,
  },
  texteVille: {
    flex: 1,
    fontSize: tailles.texteLg,
    fontWeight: '700',
    color: couleurs.textePrincipal,
  },
  badgeAffectation: {
    backgroundColor: couleurs.secondaire,
    paddingHorizontal: espacements.sm,
    paddingVertical: 4,
    borderRadius: rayons.full,
  },
  texteBadgeAffectation: {
    fontSize: tailles.texteFin,
    fontWeight: '600',
    color: couleurs.texteInverse,
    textTransform: 'uppercase',
  },
  aideChamp: {
    fontSize: tailles.texteFin,
    color: couleurs.texteDiscret,
    marginTop: espacements.xs,
    fontStyle: 'italic',
  },
  selecteurProduit: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    backgroundColor: couleurs.fond,
    borderWidth: 2,
    borderColor: couleurs.bordure,
    borderRadius: rayons.md,
    padding: espacements.md,
  },
  texteSelecteurProduit: {
    flex: 1,
    fontSize: tailles.texteBase,
    color: couleurs.textePrincipal,
  },
  placeholderSelecteur: {
    color: couleurs.texteDiscret,
  },
  conteneurInputPrix: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    backgroundColor: couleurs.fond,
    borderWidth: 2,
    borderColor: couleurs.bordure,
    borderRadius: rayons.md,
    padding: espacements.md,
  },
  inputPrix: {
    flex: 1,
    fontSize: tailles.texteXl,
    fontWeight: '700',
    color: couleurs.textePrincipal,
  },
  uniteAriary: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.texteDiscret,
  },
  boutonSoumettre: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: couleurs.secondaire,
    paddingVertical: espacements.md,
    borderRadius: rayons.md,
    marginTop: espacements.md,
    gap: espacements.sm,
    shadowColor: couleurs.secondaireFoncee,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  boutonDesactive: {
    opacity: 0.7,
  },
  texteBoutonSoumettre: {
    color: couleurs.texteInverse,
    fontSize: tailles.texteBase,
    fontWeight: '700',
  },
  carteResultat: {
    marginHorizontal: espacements.lg,
    marginTop: espacements.md,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    borderWidth: 2,
  },
  carteResultatSucces: {
    backgroundColor: couleurs.succesFond,
    borderColor: couleurs.succes,
  },
  carteResultatDoublon: {
    backgroundColor: couleurs.erreurFond,
    borderColor: couleurs.erreur,
  },
  carteResultatAlerte: {
    backgroundColor: couleurs.avertissementFond,
    borderColor: couleurs.avertissement,
  },
  entetResultat: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    marginBottom: espacements.sm,
  },
  titreResultat: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
  },
  messageResultat: {
    fontSize: tailles.texteBase,
    lineHeight: 22,
  },
  bandeauAlerte: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    backgroundColor: couleurs.avertissement,
    padding: espacements.sm,
    borderRadius: rayons.md,
    marginTop: espacements.md,
  },
  texteBandeauAlerte: {
    flex: 1,
    color: couleurs.texteInverse,
    fontSize: tailles.texteSm,
    fontWeight: '600',
  },
  detailsResultat: {
    backgroundColor: couleurs.fondSecondaire,
    padding: espacements.md,
    borderRadius: rayons.md,
    marginTop: espacements.md,
  },
  labelDetail: {
    fontSize: tailles.texteSm,
    color: couleurs.texteDiscret,
    marginBottom: 4,
  },
  valeurDetail: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
  },
  fondModal: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  contenuModal: {
    backgroundColor: couleurs.fondSecondaire,
    borderTopLeftRadius: rayons.xl,
    borderTopRightRadius: rayons.xl,
    maxHeight: '80%',
  },
  entetModal: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: espacements.lg,
    borderBottomWidth: 1,
    borderBottomColor: couleurs.bordure,
  },
  titreModal: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
    color: couleurs.textePrincipal,
  },
  boutonFermerModal: {
    padding: espacements.xs,
  },
  listeProduits: {
    padding: espacements.md,
  },
  itemProduit: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.md,
    padding: espacements.md,
    borderRadius: rayons.md,
    marginBottom: espacements.xs,
    backgroundColor: couleurs.fond,
  },
  itemProduitSelectionne: {
    backgroundColor: couleurs.secondaireTresClaire,
    borderWidth: 1,
    borderColor: couleurs.secondaire,
  },
  infoProduit: {
    flex: 1,
  },
  nomProduitFr: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.textePrincipal,
  },
  nomProduitSelectionne: {
    color: couleurs.secondaireFoncee,
  },
  nomProduitMg: {
    fontSize: tailles.texteSm,
    color: couleurs.texteDiscret,
    fontStyle: 'italic',
  },
});