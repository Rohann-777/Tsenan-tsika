import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, StyleSheet, SafeAreaView, ScrollView,
  RefreshControl, ActivityIndicator, StatusBar
} from 'react-native';
import {
  LayoutDashboard, AlertTriangle, TrendingUp, Calendar,
  MapPin, Activity, Info, Sparkles
} from 'lucide-react-native';
import { serviceTableauBord } from '../services/api';
import { utiliserAuth } from '../contexts/ContexteAuth';
import { couleurs, espacements, rayons, tailles } from '../styles/theme';

export default function EcranTableauBord() {
  const { utilisateur } = utiliserAuth();
  const [donnees, setDonnees] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [rafraichissement, setRafraichissement] = useState(false);
  const [erreur, setErreur] = useState(null);

  const chargerDonnees = useCallback(async () => {
    try {
      const reponse = await serviceTableauBord.obtenirTableauBord();
      setDonnees(reponse);
      setErreur(null);
    } catch (err) {
      setErreur('Impossible de charger le tableau de bord');
      console.error(err);
    } finally {
      setChargement(false);
      setRafraichissement(false);
    }
  }, []);

  useEffect(() => {
    chargerDonnees();
  }, [chargerDonnees]);

  const surRafraichissement = useCallback(() => {
    setRafraichissement(true);
    chargerDonnees();
  }, [chargerDonnees]);

  const formaterDate = (dateIso) => {
    const date = new Date(dateIso);
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const obtenirCouleurRang = (rang) => {
    if (rang === 1) return '#f59e0b';
    if (rang === 2) return '#94a3b8';
    if (rang === 3) return '#c2410c';
    return couleurs.primaire;
  };

  if (chargement) {
    return (
      <SafeAreaView style={styles.conteneurChargement}>
        <ActivityIndicator size="large" color={couleurs.primaire} />
        <Text style={styles.texteChargement}>Chargement des données...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.conteneur}>
      <StatusBar barStyle="light-content" backgroundColor={couleurs.primaireFoncee} />
      
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={rafraichissement}
            onRefresh={surRafraichissement}
            tintColor={couleurs.primaire}
          />
        }
      >
        
        {/* En-tête avec titre et description. */}
        <View style={styles.entete}>
          <View style={styles.entetTitreSection}>
            <LayoutDashboard size={28} color={couleurs.texteInverse} />
            <Text style={styles.titreEntete}>Tableau de bord</Text>
          </View>
          <Text style={styles.descriptionEntete}>
            Vue synthétique de l'activité du système de surveillance
          </Text>
        </View>

        {/* Compteur principal d'alertes très visible. */}
        <View style={styles.carteCompteur}>
          <View style={styles.iconeCompteur}>
            <AlertTriangle size={28} color={couleurs.erreur} />
          </View>
          <View style={styles.contenuCompteur}>
            <Text style={styles.nombreAlertes}>
              {donnees?.nombre_alertes_actives || 0}
            </Text>
            <Text style={styles.labelAlertes}>
              {donnees?.nombre_alertes_actives === 1 ? 'alerte active' : 'alertes actives'}
            </Text>
          </View>
        </View>

        {erreur && (
          <View style={styles.boiteErreur}>
            <AlertTriangle size={18} color={couleurs.erreurTexte} />
            <Text style={styles.texteErreur}>{erreur}</Text>
          </View>
        )}

        {/* Section des alertes récentes. */}
        <View style={styles.section}>
          <View style={styles.entetSection}>
            <View style={styles.entetSectionGauche}>
              <AlertTriangle size={20} color={couleurs.erreur} />
              <Text style={styles.titreSection}>Alertes récentes</Text>
            </View>
            <View style={styles.compteurBadge}>
              <Text style={styles.texteCompteurBadge}>
                {donnees?.alertes_recentes?.length || 0}
              </Text>
            </View>
          </View>

          {!donnees?.alertes_recentes || donnees.alertes_recentes.length === 0 ? (
            <View style={styles.etatVide}>
              <View style={styles.iconeEtatVide}>
                <Activity size={32} color={couleurs.succes} />
              </View>
              <Text style={styles.titreEtatVide}>Système stable</Text>
              <Text style={styles.descriptionEtatVide}>
                Aucune alerte de prix anormal n'a été déclenchée récemment.
              </Text>
            </View>
          ) : (
            <View style={styles.listeAlertes}>
              {donnees.alertes_recentes.map((alerte, index) => (
                <View key={`alerte-${alerte.id}-${index}`} style={styles.carteAlerte}>
                  <View style={styles.entetAlerte}>
                    <Text style={styles.produitAlerte}>{alerte.produit_nom}</Text>
                    <Text style={styles.villeAlerte}>à {alerte.ville_nom}</Text>
                  </View>
                  <View style={styles.dateAlerte}>
                    <Calendar size={12} color={couleurs.texteDiscret} />
                    <Text style={styles.texteDateAlerte}>
                      {formaterDate(alerte.date)}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
          )}
        </View>

        {/* Section du classement Top-5 des hausses. */}
        <View style={styles.section}>
          <View style={styles.entetSection}>
            <View style={styles.entetSectionGauche}>
              <TrendingUp size={20} color={couleurs.avertissement} />
              <Text style={styles.titreSection}>Top 5 des hausses</Text>
            </View>
            <View style={styles.compteurBadge}>
              <Text style={styles.texteCompteurBadge}>
                {donnees?.top_5_hausses?.length || 0} / 5
              </Text>
            </View>
          </View>

          {!donnees?.top_5_hausses || donnees.top_5_hausses.length === 0 ? (
            <View style={styles.etatVide}>
              <View style={styles.iconeEtatVide}>
                <Sparkles size={32} color={couleurs.info} />
              </View>
              <Text style={styles.titreEtatVide}>Marché stable</Text>
              <Text style={styles.descriptionEtatVide}>
                Aucune variation significative n'a été enregistrée récemment.
              </Text>
            </View>
          ) : (
            <View style={styles.listeTopK}>
              {donnees.top_5_hausses.map((entree, index) => (
                <View key={`topk-${entree.produit_id}-${index}`} style={styles.carteTopK}>
                  <View style={[
                    styles.rangTopK,
                    { backgroundColor: obtenirCouleurRang(entree.rang) }
                  ]}>
                    <Text style={styles.texteRang}>{entree.rang}</Text>
                  </View>
                  <View style={styles.contenuTopK}>
                    <Text style={styles.produitTopK}>{entree.produit_nom}</Text>
                    <View style={styles.variationTopK}>
                      <TrendingUp size={14} color={couleurs.erreur} />
                      <Text style={styles.texteVariation}>
                        +{entree.variation_pourcent}%
                      </Text>
                    </View>
                  </View>
                </View>
              ))}
            </View>
          )}
        </View>

        {/* Section explicative en bas. */}
        <View style={styles.sectionExplicative}>
          <View style={styles.iconeInfo}>
            <Info size={20} color={couleurs.info} />
          </View>
          <View style={styles.contenuExplicatif}>
            <Text style={styles.titreExplicatif}>Comment ça fonctionne</Text>
            <Text style={styles.texteExplicatif}>
              Le système analyse en continu les prix soumis par les agents. 
              Une alerte est déclenchée automatiquement quand la variation 
              dépasse 20% par rapport à la moyenne récente.
            </Text>
          </View>
        </View>

      </ScrollView>
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
  scrollContent: {
    paddingBottom: espacements.xl,
  },
  entete: {
    backgroundColor: couleurs.primaire,
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
  carteCompteur: {
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    marginTop: -espacements.lg,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.md,
    borderLeftWidth: 4,
    borderLeftColor: couleurs.erreur,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  iconeCompteur: {
    width: 56,
    height: 56,
    borderRadius: rayons.md,
    backgroundColor: couleurs.erreurFond,
    justifyContent: 'center',
    alignItems: 'center',
  },
  contenuCompteur: {
    flex: 1,
  },
  nombreAlertes: {
    fontSize: tailles.texteEnorme,
    fontWeight: '800',
    color: couleurs.erreur,
    lineHeight: 50,
  },
  labelAlertes: {
    fontSize: tailles.texteSm,
    color: couleurs.texteDiscret,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    fontWeight: '600',
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
  section: {
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    marginTop: espacements.md,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  entetSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: espacements.md,
    paddingBottom: espacements.sm,
    borderBottomWidth: 1,
    borderBottomColor: couleurs.bordure,
  },
  entetSectionGauche: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
  },
  titreSection: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
    color: couleurs.textePrincipal,
  },
  compteurBadge: {
    backgroundColor: couleurs.fond,
    paddingHorizontal: espacements.md,
    paddingVertical: 4,
    borderRadius: rayons.full,
  },
  texteCompteurBadge: {
    fontSize: tailles.texteSm,
    fontWeight: '600',
    color: couleurs.texteDiscret,
  },
  etatVide: {
    alignItems: 'center',
    paddingVertical: espacements.lg,
  },
  iconeEtatVide: {
    width: 64,
    height: 64,
    borderRadius: rayons.full,
    backgroundColor: couleurs.fond,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: espacements.md,
  },
  titreEtatVide: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.texteSecondaire,
    marginBottom: espacements.xs,
  },
  descriptionEtatVide: {
    fontSize: tailles.texteSm,
    color: couleurs.texteDiscret,
    textAlign: 'center',
    paddingHorizontal: espacements.md,
    lineHeight: 18,
  },
  listeAlertes: {
    gap: espacements.sm,
  },
  carteAlerte: {
    backgroundColor: couleurs.fond,
    padding: espacements.md,
    borderRadius: rayons.md,
    borderLeftWidth: 4,
    borderLeftColor: couleurs.erreur,
  },
  entetAlerte: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    marginBottom: espacements.xs,
    flexWrap: 'wrap',
  },
  produitAlerte: {
    fontSize: tailles.texteBase,
    fontWeight: '700',
    color: couleurs.erreur,
  },
  villeAlerte: {
    fontSize: tailles.texteBase,
    color: couleurs.texteSecondaire,
  },
  dateAlerte: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.xs,
    marginTop: 4,
  },
  texteDateAlerte: {
    fontSize: tailles.texteFin,
    color: couleurs.texteDiscret,
  },
  listeTopK: {
    gap: espacements.sm,
  },
  carteTopK: {
    backgroundColor: couleurs.fond,
    padding: espacements.md,
    borderRadius: rayons.md,
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.md,
  },
  rangTopK: {
    width: 40,
    height: 40,
    borderRadius: rayons.full,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  texteRang: {
    fontSize: tailles.texteBase,
    fontWeight: '800',
    color: couleurs.texteInverse,
  },
  contenuTopK: {
    flex: 1,
  },
  produitTopK: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.textePrincipal,
    marginBottom: 2,
  },
  variationTopK: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  texteVariation: {
    fontSize: tailles.texteBase,
    fontWeight: '700',
    color: couleurs.erreur,
  },
  sectionExplicative: {
    backgroundColor: couleurs.infoFond,
    marginHorizontal: espacements.lg,
    marginTop: espacements.md,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    flexDirection: 'row',
    gap: espacements.md,
    borderLeftWidth: 4,
    borderLeftColor: couleurs.info,
  },
  iconeInfo: {
    width: 40,
    height: 40,
    borderRadius: rayons.md,
    backgroundColor: 'rgba(59, 130, 246, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  contenuExplicatif: {
    flex: 1,
  },
  titreExplicatif: {
    fontSize: tailles.texteBase,
    fontWeight: '700',
    color: couleurs.infoTexte,
    marginBottom: espacements.xs,
  },
  texteExplicatif: {
    fontSize: tailles.texteSm,
    color: couleurs.infoTexte,
    lineHeight: 18,
  },
  bandeauUnite: {
  marginTop: espacements.xs,
  paddingHorizontal: espacements.md,
  paddingVertical: espacements.xs,
  backgroundColor: couleurs.infoFond,
  borderRadius: rayons.sm,
  alignSelf: 'flex-start',
  },
  texteBandeauUnite: {
  fontSize: tailles.texteSm,
  color: couleurs.infoTexte,
  fontWeight: '600',
  },
});